"""Compatibility script to seed sample products into MongoDB.
Can be run as:
    python backend/seed_sample_products.py
or
    python backend/seed_products.py
"""
import sys
from pathlib import Path

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from seed_products import run, PRODUCTS, CATALOG_FARMER_NAME
from database import check_connection, init_db, products, users

def seed_sample_products():
    run()

if __name__ == "__main__":
    seed_sample_products()
