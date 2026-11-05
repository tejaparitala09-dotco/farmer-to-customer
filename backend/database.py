"""MongoDB connection and collection helpers."""

import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "farmer_to_customer")

# MongoClient is lazy: creating it does not connect until an operation is requested.
mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
database = mongo_client[MONGODB_DATABASE]
customers_collection = database["customers"]
farmers_collection = database["farmers"]
products_collection = database["products"]
orders_collection = database["orders"]


def check_connection() -> None:
    """Raise PyMongoError when MongoDB cannot be reached."""
    mongo_client.admin.command("ping")


def ensure_indexes() -> None:
    """Create the indexes required for unique user emails."""
    customers_collection.create_index("email", unique=True)
    farmers_collection.create_index("email", unique=True)
    products_collection.create_index("farmer_id")
    products_collection.create_index([("product_name", "text"), ("category", "text")])
    orders_collection.create_index("customer_id")
    orders_collection.create_index("farmer_ids")


def get_collection(role: str) -> Collection:
    """Return the collection for a validated user role."""
    if role == "customer":
        return customers_collection
    if role == "farmer":
        return farmers_collection
    raise ValueError(f"Unsupported user role: {role}")


def find_user_by_email(email: str) -> dict | None:
    """Find a user in either role collection."""
    customer = customers_collection.find_one({"email": email})
    if customer is not None:
        return customer
    return farmers_collection.find_one({"email": email})


__all__ = [
    "PyMongoError",
    "check_connection",
    "ensure_indexes",
    "find_user_by_email",
    "get_collection",
    "mongo_client",
    "orders_collection",
    "products_collection",
]
