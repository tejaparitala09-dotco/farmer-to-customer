"""Seed the real starter catalog into MongoDB.

Run from the project root with: py -3 backend/seed_products.py
Existing records with these stable IDs are updated instead of duplicated.
"""

from datetime import datetime, timezone

try:
    from .database import check_connection, ensure_indexes, products_collection
except ImportError:
    from database import check_connection, ensure_indexes, products_collection


CATALOG_FARMER_ID = "catalog-green-valley-farm"
CATALOG_FARMER_NAME = "Green Valley Farm"

PRODUCTS = [
    {
        "id": "catalog-tomato",
        "product_name": "Tomato",
        "category": "Vegetables",
        "price": 2.40,
        "unit": "kg",
        "quantity": 100,
        "description": "Vine-ripened tomatoes with a bright, juicy flavor for everyday cooking and salads.",
        "image_url": "https://images.unsplash.com/photo-1546094096-0df4bcaaa337?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-potato",
        "product_name": "Potato",
        "category": "Vegetables",
        "price": 1.80,
        "unit": "kg",
        "quantity": 120,
        "description": "Firm, versatile potatoes harvested fresh for roasting, mashing, and home cooking.",
        "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-onion",
        "product_name": "Onion",
        "category": "Vegetables",
        "price": 2.10,
        "unit": "kg",
        "quantity": 110,
        "description": "Golden cooking onions with a balanced sweetness and a crisp, dry finish.",
        "image_url": "https://images.unsplash.com/photo-1508747703725-719777637510?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-carrot",
        "product_name": "Carrot",
        "category": "Vegetables",
        "price": 2.60,
        "unit": "bunch",
        "quantity": 80,
        "description": "Crunchy, naturally sweet carrots bundled soon after harvest.",
        "image_url": "https://images.unsplash.com/photo-1445282768818-728615cc910a?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-brinjal",
        "product_name": "Brinjal",
        "category": "Vegetables",
        "price": 2.80,
        "unit": "kg",
        "quantity": 70,
        "description": "Glossy purple brinjal with tender flesh, ideal for curries, grills, and bakes.",
        "image_url": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-cabbage",
        "product_name": "Cabbage",
        "category": "Vegetables",
        "price": 1.90,
        "unit": "piece",
        "quantity": 60,
        "description": "Tightly packed green cabbage with crisp leaves for slaws and stir-fries.",
        "image_url": "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-cauliflower",
        "product_name": "Cauliflower",
        "category": "Vegetables",
        "price": 2.75,
        "unit": "piece",
        "quantity": 55,
        "description": "Fresh white cauliflower heads with firm florets and mild flavor.",
        "image_url": "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-spinach",
        "product_name": "Spinach",
        "category": "Vegetables",
        "price": 2.25,
        "unit": "bunch",
        "quantity": 90,
        "description": "Dark green tender spinach leaves, picked for soups, sautés, and fresh dishes.",
        "image_url": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-lady-finger",
        "product_name": "Lady Finger",
        "category": "Vegetables",
        "price": 3.20,
        "unit": "kg",
        "quantity": 65,
        "description": "Young, tender lady finger pods with a clean snap and delicate flavor.",
        "image_url": "https://images.unsplash.com/photo-1628773822503-930a7eaecf80?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-green-chilli",
        "product_name": "Green Chilli",
        "category": "Vegetables",
        "price": 4.50,
        "unit": "kg",
        "quantity": 45,
        "description": "Fresh green chillies with a lively heat for chutneys, curries, and pickles.",
        "image_url": "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-apple",
        "product_name": "Apple",
        "category": "Fruits",
        "price": 4.80,
        "unit": "kg",
        "quantity": 75,
        "description": "Crisp, naturally sweet apples selected for a refreshing bite.",
        "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-banana",
        "product_name": "Banana",
        "category": "Fruits",
        "price": 1.90,
        "unit": "kg",
        "quantity": 100,
        "description": "Naturally creamy bananas delivered at the perfect stage for ripening at home.",
        "image_url": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-orange",
        "product_name": "Orange",
        "category": "Fruits",
        "price": 3.60,
        "unit": "kg",
        "quantity": 80,
        "description": "Juicy oranges with a bright citrus aroma and refreshing sweetness.",
        "image_url": "https://images.unsplash.com/photo-1547514701-42782101795e?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-mango",
        "product_name": "Mango",
        "category": "Fruits",
        "price": 5.50,
        "unit": "kg",
        "quantity": 65,
        "description": "Fragrant, golden mangoes with rich tropical sweetness.",
        "image_url": "https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-papaya",
        "product_name": "Papaya",
        "category": "Fruits",
        "price": 2.90,
        "unit": "kg",
        "quantity": 50,
        "description": "Soft, sun-ripened papaya with smooth texture and mellow sweetness.",
        "image_url": "https://images.unsplash.com/photo-1526318472351-c75fcf070305?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-watermelon",
        "product_name": "Watermelon",
        "category": "Fruits",
        "price": 0.90,
        "unit": "kg",
        "quantity": 90,
        "description": "Cool, juicy watermelon grown for a crisp and refreshing summer slice.",
        "image_url": "https://images.unsplash.com/photo-1563114773-84221bd62daa?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-pomegranate",
        "product_name": "Pomegranate",
        "category": "Fruits",
        "price": 6.40,
        "unit": "kg",
        "quantity": 45,
        "description": "Ruby-red pomegranates filled with bright, jewel-like arils.",
        "image_url": "https://images.unsplash.com/photo-1541344999736-83eca272f6fc?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-grapes",
        "product_name": "Grapes",
        "category": "Fruits",
        "price": 5.20,
        "unit": "kg",
        "quantity": 55,
        "description": "Plump table grapes with a fresh snap and naturally sweet finish.",
        "image_url": "https://images.unsplash.com/photo-1537640538966-79f369143f8f?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-guava",
        "product_name": "Guava",
        "category": "Fruits",
        "price": 3.40,
        "unit": "kg",
        "quantity": 40,
        "description": "Aromatic guavas with fragrant flesh and a gently floral sweetness.",
        "image_url": "https://images.unsplash.com/photo-1536511132770-e5058c7e8c46?auto=format&fit=crop&w=800&q=85",
    },
    {
        "id": "catalog-pineapple",
        "product_name": "Pineapple",
        "category": "Fruits",
        "price": 3.20,
        "unit": "piece",
        "quantity": 35,
        "description": "Golden pineapple with juicy tropical flavor and a naturally bright aroma.",
        "image_url": "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?auto=format&fit=crop&w=800&q=85",
    },
]


def seed_products() -> None:
    check_connection()
    ensure_indexes()
    now = datetime.now(timezone.utc)
    for product in PRODUCTS:
        document = {
            **product,
            "farmer_id": CATALOG_FARMER_ID,
            "farmer_name": CATALOG_FARMER_NAME,
            "created_at": now,
            "updated_at": now,
        }
        products_collection.update_one(
            {"id": product["id"]},
            {"$set": document},
            upsert=True,
        )
    print(f"Seeded {len(PRODUCTS)} products into MongoDB.")


if __name__ == "__main__":
    seed_products()
