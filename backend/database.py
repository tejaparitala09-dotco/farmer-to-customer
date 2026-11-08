import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env from backend directory or project root
load_dotenv(Path(__file__).resolve().parent / ".env")
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "farmer_to_customer")

client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=1000,
    connectTimeoutMS=1000,
    socketTimeoutMS=1000
)
db = client[MONGODB_DATABASE]

users = db.users
products = db.products
orders = db.orders

# Backwards compatibility aliases
users_collection = users
products_collection = products
orders_collection = orders

def check_connection():
    if os.getenv("TESTING") == "1":
        return True
    try:
        client.admin.command("ping")
        return True
    except Exception:
        return False

def init_db():
    if os.getenv("TESTING") == "1":
        return
    if not check_connection():
        print("[Database] MongoDB not currently reachable; index creation deferred.")
        return
    try:
        users.create_index("email", unique=True)
        products.create_index("seed_key", unique=True, sparse=True)
        products.create_index("product_name")
        products.create_index("category")
        products.create_index("farmer_id")
        orders.create_index("customer_id")
        orders.create_index("farmer_id")
        orders.create_index("created_at")
        print("[Database] Indexes verified successfully.")
    except Exception as e:
        print(f"[Database] Warning during index creation: {e}")
