import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(Path(__file__).with_name(".env"))
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI must be configured")
if not MONGODB_DATABASE:
    raise RuntimeError("MONGODB_DATABASE must be configured")
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=3000)
db = client[MONGODB_DATABASE]
users = db.users
products = db.products
orders = db.orders

def init_db():
    users.create_index("email", unique=True)
    products.create_index("seed_key", unique=True, sparse=True)
    orders.create_index("customer_id")
    orders.create_index("farmer_id")
