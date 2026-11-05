"""Seed the 20 requested agricultural sample products into MongoDB.

Run from the project root with: py -3 backend/seed_sample_products.py
Existing records with these stable IDs are updated instead of duplicated.
"""

from datetime import datetime, timezone

try:
    from .database import check_connection, ensure_indexes, products_collection
    from .seed_products import CATALOG_FARMER_ID, CATALOG_FARMER_NAME, PRODUCTS
except ImportError:
    from database import check_connection, ensure_indexes, products_collection
    from seed_products import CATALOG_FARMER_ID, CATALOG_FARMER_NAME, PRODUCTS


SAMPLE_PRODUCT_IDS = (
    "catalog-tomato",
    "catalog-potato",
    "catalog-onion",
    "catalog-carrot",
    "catalog-brinjal",
    "catalog-cabbage",
    "catalog-cauliflower",
    "catalog-spinach",
    "catalog-lady-finger",
    "catalog-green-chilli",
    "catalog-apple",
    "catalog-banana",
    "catalog-orange",
    "catalog-mango",
    "catalog-papaya",
    "catalog-watermelon",
    "catalog-pomegranate",
    "catalog-grapes",
    "catalog-guava",
    "catalog-pineapple",
)


def seed_sample_products() -> None:
    products_by_id = {product["id"]: product for product in PRODUCTS}
    sample_products = [products_by_id[product_id] for product_id in SAMPLE_PRODUCT_IDS]

    check_connection()
    ensure_indexes()
    now = datetime.now(timezone.utc)
    for product in sample_products:
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
    print(f"Seeded {len(sample_products)} sample products into MongoDB.")


if __name__ == "__main__":
    seed_sample_products()
