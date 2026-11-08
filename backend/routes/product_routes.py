from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from database import products, users
from models import ProductRequest
from auth import require_role, current_user

router = APIRouter(prefix="/api/products", tags=["products"])
def clean(item):
    item["id"] = str(item.pop("_id")); item["farmer_id"] = str(item["farmer_id"]); return item

def find_product(product_id):
    try: item = products.find_one({"_id": ObjectId(product_id)})
    except Exception: item = None
    if not item: raise HTTPException(404, "Product not found")
    return item

@router.get("")
def list_products(search: str = "", category: str = ""):
    query = {}
    if search: query["$or"] = [{"product_name": {"$regex": search, "$options": "i"}}, {"description": {"$regex": search, "$options": "i"}}]
    if category: query["category"] = category
    return [clean(x) for x in products.find(query).sort("product_name", 1)]

@router.get("/farmer/mine")
def my_products(farmer=Depends(require_role("farmer"))): return [clean(x) for x in products.find({"farmer_id": ObjectId(farmer["id"])})]

@router.get("/{product_id}")
def get_product(product_id: str): return clean(find_product(product_id))

@router.post("")
def add_product(data: ProductRequest, farmer=Depends(require_role("farmer"))):
    item = data.model_dump(); item.update({"farmer_id": ObjectId(farmer["id"]), "created_at": datetime.now(timezone.utc)})
    result = products.insert_one(item); item["_id"] = result.inserted_id
    return clean(item)

@router.put("/{product_id}")
def edit_product(product_id: str, data: ProductRequest, farmer=Depends(require_role("farmer"))):
    item = find_product(product_id)
    if str(item["farmer_id"]) != farmer["id"]: raise HTTPException(403, "You can only edit your own products")
    products.update_one({"_id": item["_id"]}, {"$set": data.model_dump()})
    return clean(find_product(product_id))

@router.delete("/{product_id}")
def delete_product(product_id: str, farmer=Depends(require_role("farmer"))):
    item = find_product(product_id)
    if str(item["farmer_id"]) != farmer["id"]: raise HTTPException(403, "You can only delete your own products")
    products.delete_one({"_id": item["_id"]}); return {"message": "Product deleted"}

