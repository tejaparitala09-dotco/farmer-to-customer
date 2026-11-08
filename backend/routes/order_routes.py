from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from database import orders, products, users
from models import CreateOrderRequest, StatusRequest
from auth import require_role

router = APIRouter(prefix="/api/orders", tags=["orders"])
def clean(order):
    order["id"] = str(order.pop("_id")); order["order_id"] = order["id"]
    order["customer_id"] = str(order["customer_id"]); order["farmer_id"] = str(order["farmer_id"])
    return order

@router.post("")
def create_order(data: CreateOrderRequest, customer=Depends(require_role("customer"))):
    grouped = {}
    for requested in data.items:
        try: product = products.find_one({"_id": ObjectId(requested.product_id)})
        except Exception: product = None
        if not product: raise HTTPException(404, "A selected product no longer exists")
        if requested.quantity > product["quantity"]: raise HTTPException(400, f"Not enough stock for {product['product_name']}")
        farmer = str(product["farmer_id"]); grouped.setdefault(farmer, []).append((product, requested.quantity))
    created = []
    for farmer_id, entries in grouped.items():
        line_items=[]; total=0
        for product, qty in entries:
            total += product["price"] * qty
            line_items.append({"product_id": str(product["_id"]), "product_name": product["product_name"], "quantity": qty, "price": product["price"], "unit": product["unit"]})
            products.update_one({"_id": product["_id"]}, {"$inc": {"quantity": -qty}})
        order={"customer_id": ObjectId(customer["id"]), "farmer_id": ObjectId(farmer_id), "products": line_items, "total_amount": round(total,2), "delivery_address": data.delivery_address.model_dump(), "status":"Pending", "created_at":datetime.now(timezone.utc)}
        result=orders.insert_one(order); order["_id"]=result.inserted_id; created.append(clean(order))
    return created

@router.get("/my-orders")
def my_orders(customer=Depends(require_role("customer"))): return [clean(x) for x in orders.find({"customer_id": ObjectId(customer["id"])}).sort("created_at", -1)]

@router.get("/farmer-orders")
def farmer_orders(farmer=Depends(require_role("farmer"))):
    result=[]
    for order in orders.find({"farmer_id": ObjectId(farmer["id"])}).sort("created_at", -1):
        order=clean(order); customer=users.find_one({"_id": ObjectId(order["customer_id"])})
        order["customer"]={"name":customer.get("name",""),"phone":customer.get("phone","")} if customer else {}; result.append(order)
    return result

@router.put("/{order_id}/status")
def update_status(order_id: str, data: StatusRequest, farmer=Depends(require_role("farmer"))):
    allowed={"Pending","Confirmed","Packed","Out for Delivery","Delivered","Cancelled"}
    if data.status not in allowed: raise HTTPException(400,"Invalid order status")
    try: oid=ObjectId(order_id)
    except Exception: raise HTTPException(404,"Order not found")
    if not orders.find_one({"_id":oid,"farmer_id":ObjectId(farmer["id"])}): raise HTTPException(403,"This order is not related to you")
    orders.update_one({"_id":oid},{"$set":{"status":data.status}}); return {"message":"Status updated"}
