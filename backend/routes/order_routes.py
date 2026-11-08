from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from database import orders, products, users
from models import CreateOrderRequest, StatusRequest
from auth import require_role

router = APIRouter(prefix="/api/orders", tags=["orders"])

def clean(order: dict) -> dict:
    if not order:
        return order
    record = dict(order)
    if "_id" in record:
        record["id"] = str(record.pop("_id"))
    elif "id" not in record:
        record["id"] = ""
    record["order_id"] = record["id"]
    record["customer_id"] = str(record.get("customer_id", ""))
    record["farmer_id"] = str(record.get("farmer_id", ""))
    return record

@router.post("")
def create_order(data: CreateOrderRequest, customer: dict = Depends(require_role("customer"))):
    if not data.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Fetch products and check stock
    grouped = {}
    for requested in data.items:
        product = None
        try:
            product = products.find_one({"_id": ObjectId(requested.product_id)})
        except Exception:
            pass
        if not product:
            product = products.find_one({"_id": requested.product_id}) or products.find_one({"id": requested.product_id})

        if not product:
            raise HTTPException(status_code=404, detail="One or more selected products no longer exist")

        available = float(product.get("quantity", 0))
        if requested.quantity > available:
            raise HTTPException(
                status_code=400,
                detail=f"Only {available} {product.get('unit','units')} available for {product['product_name']}"
            )

        farmer_key = str(product.get("farmer_id", "default_farmer"))
        grouped.setdefault(farmer_key, []).append((product, requested.quantity))

    created = []
    now = datetime.now(timezone.utc)

    for farmer_id_str, entries in grouped.items():
        line_items = []
        total = 0.0
        for product, qty in entries:
            price = float(product.get("price", 0))
            subtotal = price * qty
            total += subtotal
            line_items.append({
                "product_id": str(product.get("_id", product.get("id"))),
                "product_name": product.get("product_name", ""),
                "quantity": qty,
                "price": price,
                "unit": product.get("unit", "kg"),
                "image_url": product.get("image_url", ""),
            })
            # Decrement stock
            products.update_one(
                {"_id": product["_id"]},
                {"$inc": {"quantity": -qty}}
            )

        try:
            farmer_oid = ObjectId(farmer_id_str)
        except Exception:
            farmer_oid = farmer_id_str

        try:
            customer_oid = ObjectId(customer["id"])
        except Exception:
            customer_oid = customer["id"]

        order_record = {
            "customer_id": customer_oid,
            "farmer_id": farmer_oid,
            "products": line_items,
            "total_amount": round(total, 2),
            "delivery_address": data.delivery_address.model_dump(),
            "status": "Pending",
            "created_at": now,
            "updated_at": now,
        }
        res = orders.insert_one(order_record)
        order_record["_id"] = res.inserted_id
        created.append(clean(order_record))

    return created

@router.get("/my-orders")
def my_orders(customer: dict = Depends(require_role("customer"))):
    ids = [customer["id"]]
    try:
        ids.append(ObjectId(customer["id"]))
    except Exception:
        pass

    cursor = orders.find({"customer_id": {"$in": ids}}).sort("created_at", -1)
    return [clean(x) for x in cursor]

@router.get("/farmer-orders")
def farmer_orders(farmer: dict = Depends(require_role("farmer"))):
    ids = [farmer["id"]]
    try:
        ids.append(ObjectId(farmer["id"]))
    except Exception:
        pass

    result = []
    cursor = orders.find({"farmer_id": {"$in": ids}}).sort("created_at", -1)
    for raw_order in cursor:
        order = clean(raw_order)
        cust_id = order.get("customer_id")
        user_record = None
        if cust_id:
            try:
                user_record = users.find_one({"_id": ObjectId(cust_id)})
            except Exception:
                user_record = users.find_one({"_id": cust_id})

        if user_record:
            order["customer"] = {
                "name": user_record.get("name", "Customer"),
                "phone": user_record.get("phone", ""),
                "email": user_record.get("email", ""),
            }
        else:
            addr = order.get("delivery_address", {})
            order["customer"] = {
                "name": addr.get("full_name", "Customer"),
                "phone": addr.get("phone", ""),
                "email": "",
            }
        result.append(order)
    return result

@router.put("/{order_id}/status")
def update_status(order_id: str, data: StatusRequest, farmer: dict = Depends(require_role("farmer"))):
    allowed = {"Pending", "Confirmed", "Packed", "Shipped", "Out for Delivery", "Delivered", "Cancelled"}
    if data.status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{data.status}'. Allowed: {', '.join(allowed)}"
        )

    try:
        oid = ObjectId(order_id)
        query = {"_id": oid}
    except Exception:
        query = {"_id": order_id}

    farmer_ids = [farmer["id"]]
    try:
        farmer_ids.append(ObjectId(farmer["id"]))
    except Exception:
        pass

    order = orders.find_one({"$and": [query, {"farmer_id": {"$in": farmer_ids}}]})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or not assigned to you")

    orders.update_one(query, {"$set": {"status": data.status, "updated_at": datetime.now(timezone.utc)}})
    return {"message": "Status updated successfully", "status": data.status}
