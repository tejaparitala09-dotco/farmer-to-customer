from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from database import products, users
from models import ProductRequest
from auth import require_role, current_user

router = APIRouter(tags=["products"])

def clean(item: dict) -> dict:
    if not item:
        return item
    record = dict(item)
    if "_id" in record:
        record["id"] = str(record.pop("_id"))
    elif "id" not in record:
        record["id"] = ""
    record["farmer_id"] = str(record.get("farmer_id", ""))
    if "farmer_name" not in record or not record["farmer_name"]:
        record["farmer_name"] = "Green Valley Farm"
    return record

def find_product(product_id: str) -> dict:
    item = None
    try:
        item = products.find_one({"_id": ObjectId(product_id)})
    except Exception:
        pass
    if not item:
        item = products.find_one({"_id": product_id}) or products.find_one({"id": product_id})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return item

@router.get("/api/products")
def list_products(search: str = "", category: str = ""):
    query = {}
    if search:
        query["$or"] = [
            {"product_name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"category": {"$regex": search, "$options": "i"}},
        ]
    if category and category.lower() != "all":
        query["category"] = {"$regex": f"^{category}$", "$options": "i"}

    cursor = products.find(query).sort("product_name", 1)
    return [clean(p) for p in cursor]

@router.get("/api/products/farmer/mine")
def my_products(farmer: dict = Depends(require_role("farmer"))):
    farmer_ids = [farmer["id"]]
    try:
        farmer_ids.append(ObjectId(farmer["id"]))
    except Exception:
        pass
    cursor = products.find({"farmer_id": {"$in": farmer_ids}}).sort("created_at", -1)
    return [clean(p) for p in cursor]

@router.get("/api/farmer/products")
def farmer_products_alias(farmer: dict = Depends(require_role("farmer"))):
    return my_products(farmer)

@router.get("/api/products/{product_id}")
def get_product(product_id: str):
    return clean(find_product(product_id))

@router.post("/api/products")
def add_product(data: ProductRequest, farmer: dict = Depends(require_role("farmer"))):
    item = data.model_dump()
    try:
        farmer_oid = ObjectId(farmer["id"])
    except Exception:
        farmer_oid = farmer["id"]

    item.update({
        "farmer_id": farmer_oid,
        "farmer_name": farmer.get("name", "Local Farm"),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    })
    result = products.insert_one(item)
    item["_id"] = result.inserted_id
    return clean(item)

@router.put("/api/products/{product_id}")
def edit_product(product_id: str, data: ProductRequest, farmer: dict = Depends(require_role("farmer"))):
    item = find_product(product_id)
    if str(item.get("farmer_id")) != farmer["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit products you published"
        )
    update_data = data.model_dump()
    update_data["updated_at"] = datetime.now(timezone.utc)
    products.update_one({"_id": item["_id"]}, {"$set": update_data})
    return clean(find_product(product_id))

@router.delete("/api/products/{product_id}")
def delete_product(product_id: str, farmer: dict = Depends(require_role("farmer"))):
    item = find_product(product_id)
    if str(item.get("farmer_id")) != farmer["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete products you published"
        )
    products.delete_one({"_id": item["_id"]})
    return {"message": "Product successfully deleted"}
