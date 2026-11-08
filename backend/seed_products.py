import os
import secrets
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
load_dotenv()

from database import users, products, init_db, check_connection
from auth import hash_password

PRODUCTS = [
    # Vegetables
    {
        "id": "catalog-tomato",
        "seed_key": "tomato",
        "product_name": "Vine Ripe Tomatoes",
        "category": "Vegetables",
        "price": 38.0,
        "unit": "kg",
        "quantity": 95.0,
        "description": "Naturally ripened on the vine, firm, juicy and rich in lycopene. Directly from organic polyhouses.",
        "image_url": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=800",
    },
    {
        "id": "catalog-potato",
        "seed_key": "potato",
        "product_name": "Farm Fresh Potatoes",
        "category": "Vegetables",
        "price": 32.0,
        "unit": "kg",
        "quantity": 180.0,
        "description": "Earthy, firm golden potatoes harvested this week. Excellent for curries, bakes, and roasting.",
        "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=800",
    },
    {
        "id": "catalog-onion",
        "seed_key": "onion",
        "product_name": "Red Globe Onions",
        "category": "Vegetables",
        "price": 42.0,
        "unit": "kg",
        "quantity": 150.0,
        "description": "Pungent, sweet-layered red onions cured under gentle sun to preserve natural shelf life.",
        "image_url": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=800",
    },
    {
        "id": "catalog-carrot",
        "seed_key": "carrot",
        "product_name": "Crunchy Sweet Carrots",
        "category": "Vegetables",
        "price": 48.0,
        "unit": "kg",
        "quantity": 80.0,
        "description": "Crisp, sweet winter carrots washed gently in pure spring water. Perfect for salads and juices.",
        "image_url": "https://images.unsplash.com/photo-1445282768818-728615cc910a?w=800",
    },
    {
        "id": "catalog-brinjal",
        "seed_key": "brinjal",
        "product_name": "Tender Purple Brinjal",
        "category": "Vegetables",
        "price": 40.0,
        "unit": "kg",
        "quantity": 60.0,
        "description": "Glossy tender eggplants with delicate skin and creamy flesh. Picked at sunrise.",
        "image_url": "https://images.unsplash.com/photo-1528825871115-3581a5387919?w=800",
    },
    {
        "id": "catalog-cabbage",
        "seed_key": "cabbage",
        "product_name": "Crisp Green Cabbage",
        "category": "Vegetables",
        "price": 28.0,
        "unit": "kg",
        "quantity": 70.0,
        "description": "Tightly packed green cabbage heads with sweet, crunchy leaves. Grown without harsh sprays.",
        "image_url": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=800",
    },
    {
        "id": "catalog-cauliflower",
        "seed_key": "cauliflower",
        "product_name": "Snowball Cauliflower",
        "category": "Vegetables",
        "price": 45.0,
        "unit": "piece",
        "quantity": 50.0,
        "description": "Dense, milky-white florets protected by broad green leaves. Fresh and pesticide-free.",
        "image_url": "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=800",
    },
    {
        "id": "catalog-spinach",
        "seed_key": "spinach",
        "product_name": "Fresh Garden Palak (Spinach)",
        "category": "Vegetables",
        "price": 25.0,
        "unit": "bunch",
        "quantity": 110.0,
        "description": "Young tender spinach leaves brimming with iron and vitality. Harvested daily at dawn.",
        "image_url": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=800",
    },
    {
        "id": "catalog-green-chilli",
        "seed_key": "green chilli",
        "product_name": "Spicy Green Chillies",
        "category": "Vegetables",
        "price": 75.0,
        "unit": "kg",
        "quantity": 40.0,
        "description": "Fiery aromatic green chillies with a vibrant crunch. Direct from Guntur farm beds.",
        "image_url": "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=800",
    },
    {
        "id": "catalog-capsicum",
        "seed_key": "capsicum",
        "product_name": "Bell Peppers (Capsicum)",
        "category": "Vegetables",
        "price": 65.0,
        "unit": "kg",
        "quantity": 55.0,
        "description": "Thick-walled, crunchy green bell peppers loaded with vitamin C.",
        "image_url": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=800",
    },
    {
        "id": "catalog-cucumber",
        "seed_key": "cucumber",
        "product_name": "Crisp Field Cucumbers",
        "category": "Vegetables",
        "price": 35.0,
        "unit": "kg",
        "quantity": 85.0,
        "description": "Hydrating, thin-skinned cucumbers. Cool, crunchy, and perfect for hot afternoons.",
        "image_url": "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=800",
    },
    {
        "id": "catalog-lady-finger",
        "seed_key": "lady finger",
        "product_name": "Tender Okra (Lady Finger)",
        "category": "Vegetables",
        "price": 52.0,
        "unit": "kg",
        "quantity": 65.0,
        "description": "Small, tender non-fibrous okra pods harvested young for maximum tenderness.",
        "image_url": "https://images.unsplash.com/photo-1425543103986-22abb7d7e8d2?w=800",
    },

    # Fruits
    {
        "id": "catalog-apple",
        "seed_key": "apple",
        "product_name": "Kinnaur Mountain Apples",
        "category": "Fruits",
        "price": 135.0,
        "unit": "kg",
        "quantity": 75.0,
        "description": "Crisp, sweet-tart Himalayan apples with natural wax and unblemished mountain skin.",
        "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
    },
    {
        "id": "catalog-banana",
        "seed_key": "banana",
        "product_name": "Yelakki Sweet Bananas",
        "category": "Fruits",
        "price": 58.0,
        "unit": "dozen",
        "quantity": 90.0,
        "description": "Naturally ripened miniature Yelakki bananas known for exceptional honey-sweet flavour.",
        "image_url": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=800",
    },
    {
        "id": "catalog-mango",
        "seed_key": "mango",
        "product_name": "Alphonso Royal Mangoes",
        "category": "Fruits",
        "price": 180.0,
        "unit": "kg",
        "quantity": 50.0,
        "description": "The king of fruits. Luscious golden pulp, carbide-free tree ripened with floral aroma.",
        "image_url": "https://images.unsplash.com/photo-1553279768-865429fa0078?w=800",
    },
    {
        "id": "catalog-orange",
        "seed_key": "orange",
        "product_name": "Nagpur Juicy Oranges",
        "category": "Fruits",
        "price": 78.0,
        "unit": "kg",
        "quantity": 100.0,
        "description": "Sun-kissed, easy-peel oranges brimming with tangy-sweet citrus juice.",
        "image_url": "https://images.unsplash.com/photo-1582979512210-99b6a53386f9?w=800",
    },
    {
        "id": "catalog-papaya",
        "seed_key": "papaya",
        "product_name": "Red Lady Sweet Papaya",
        "category": "Fruits",
        "price": 45.0,
        "unit": "kg",
        "quantity": 60.0,
        "description": "Deep salmon-orange flesh, aromatic, buttery smooth, and naturally digestive.",
        "image_url": "https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?w=800",
    },
    {
        "id": "catalog-pomegranate",
        "seed_key": "pomegranate",
        "product_name": "Bhagwa Ruby Pomegranate",
        "category": "Fruits",
        "price": 145.0,
        "unit": "kg",
        "quantity": 65.0,
        "description": "Deep red soft-seeded arils bursting with rich antioxidant-packed juice.",
        "image_url": "https://images.unsplash.com/photo-1541344999736-83eca272f6fc?w=800",
    },
    {
        "id": "catalog-watermelon",
        "seed_key": "watermelon",
        "product_name": "Striped Sugar Watermelon",
        "category": "Fruits",
        "price": 35.0,
        "unit": "kg",
        "quantity": 120.0,
        "description": "Crisp red heart, sweet and deeply hydrating. Grown on fertile riverbank soils.",
        "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=800",
    },
    {
        "id": "catalog-grapes",
        "seed_key": "grapes",
        "product_name": "Nashik Seedless Green Grapes",
        "category": "Fruits",
        "price": 95.0,
        "unit": "kg",
        "quantity": 70.0,
        "description": "Crisp, thin-skinned table grapes with refreshing sweetness and snappy texture.",
        "image_url": "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=800",
    },

    # Grains & Millets & Grocery
    {
        "id": "catalog-rice",
        "seed_key": "rice",
        "product_name": "Aged Traditional Basmati Rice",
        "category": "Grains",
        "price": 85.0,
        "unit": "kg",
        "quantity": 200.0,
        "description": "Long-grain aromatic rice aged for 18 months in traditional granaries for slender fluffy grains.",
        "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=800",
    },
    {
        "id": "catalog-wheat",
        "seed_key": "wheat",
        "product_name": "Sharbati Golden Wheat",
        "category": "Grains",
        "price": 55.0,
        "unit": "kg",
        "quantity": 180.0,
        "description": "Naturally golden Sharbati wheat grains from Madhya Pradesh black soil. Yields soft, sweet rotis.",
        "image_url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800",
    },
    {
        "id": "catalog-ragi",
        "seed_key": "ragi",
        "product_name": "Organic Finger Millet (Ragi)",
        "category": "Millets",
        "price": 62.0,
        "unit": "kg",
        "quantity": 110.0,
        "description": "Ancient calcium-rich superfood grain cultivated using traditional dryland rain-fed methods.",
        "image_url": "https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=800",
    },
    {
        "id": "catalog-moong-dal",
        "seed_key": "moong dal",
        "product_name": "Unpolished Yellow Moong Dal",
        "category": "Pulses",
        "price": 118.0,
        "unit": "kg",
        "quantity": 90.0,
        "description": "Wholesome, unpolished split moong lentils retaining natural dietary fiber and fast-cooking goodness.",
        "image_url": "https://images.unsplash.com/photo-1515543904379-3d757afe72e4?w=800",
    },
    {
        "id": "catalog-turmeric",
        "seed_key": "turmeric",
        "product_name": "High-Curcumin Salem Turmeric",
        "category": "Spices",
        "price": 165.0,
        "unit": "kg",
        "quantity": 60.0,
        "description": "Pure sun-dried golden turmeric with over 5% natural curcumin content. No artificial dyes.",
        "image_url": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=800",
    },
    {
        "id": "catalog-honey",
        "seed_key": "honey",
        "product_name": "Raw Wildflower Forest Honey",
        "category": "Grocery",
        "price": 280.0,
        "unit": "bottle",
        "quantity": 45.0,
        "description": "Unpasteurized raw honey harvested ethically from forest apiaries. Naturally unfiltered.",
        "image_url": "https://images.unsplash.com/photo-1587049352851-8d4e89133924?w=800",
    },
    {
        "id": "catalog-milk",
        "seed_key": "milk",
        "product_name": "Pure A2 Farm Cow Milk",
        "category": "Dairy",
        "price": 68.0,
        "unit": "litre",
        "quantity": 80.0,
        "description": "Fresh morning milk from grass-fed Desi cows, unadulterated and chilled immediately.",
        "image_url": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=800",
    },
    {
        "id": "catalog-eggs",
        "seed_key": "eggs",
        "product_name": "Free-Range Pasture Eggs",
        "category": "Dairy",
        "price": 90.0,
        "unit": "dozen",
        "quantity": 60.0,
        "description": "Brown eggs from pasture-raised hens roaming freely on natural herbal grasslands.",
        "image_url": "https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=800",
    },
]

CATALOG_FARMER_NAME = "Green Valley Farm"

def run():
    print("[Seed] Initializing database indexes...")
    init_db()

    farmer_password = os.getenv("SEED_FARMER_PASSWORD") or secrets.token_urlsafe(24)
    customer_password = os.getenv("SEED_CUSTOMER_PASSWORD") or secrets.token_urlsafe(24)

    # Create / Update default Farmer account
    farmer_email = "farmer@farm.com"
    farmer = users.find_one({"email": farmer_email})
    if not farmer:
        farmer_data = {
            "name": CATALOG_FARMER_NAME,
            "email": farmer_email,
            "password_hash": hash_password(farmer_password),
            "phone": "+91 9876543210",
            "role": "farmer",
            "created_at": datetime.now(timezone.utc),
        }
        res = users.insert_one(farmer_data)
        farmer_data["_id"] = res.inserted_id
        farmer = farmer_data
        print(f"[Seed] Created farmer account: {farmer_email}")
    else:
        print(f"[Seed] Farmer account exists: {farmer_email}")

    # Also seed legacy seed.farmer@example.com for backward compatibility
    legacy_farmer = users.find_one({"email": "seed.farmer@example.com"})
    if not legacy_farmer:
        users.insert_one({
            "name": CATALOG_FARMER_NAME,
            "email": "seed.farmer@example.com",
            "password_hash": hash_password(farmer_password),
            "phone": "9000000000",
            "role": "farmer",
            "created_at": datetime.now(timezone.utc),
        })

    # Create / Update default Customer account
    cust_email = "customer@fresh.com"
    customer = users.find_one({"email": cust_email})
    if not customer:
        customer_data = {
            "name": "Priya Sharma",
            "email": cust_email,
            "password_hash": hash_password(customer_password),
            "phone": "+91 9123456789",
            "role": "customer",
            "created_at": datetime.now(timezone.utc),
        }
        users.insert_one(customer_data)
        print(f"[Seed] Created customer account: {cust_email}")
    else:
        print(f"[Seed] Customer account exists: {cust_email}")

    farmer_id = farmer["_id"]
    seeded_count = 0
    now = datetime.now(timezone.utc)

    for item in PRODUCTS:
        doc = {
            "seed_key": item["seed_key"],
            "product_name": item["product_name"],
            "category": item["category"],
            "price": item["price"],
            "unit": item["unit"],
            "quantity": item["quantity"],
            "description": item["description"],
            "image_url": item["image_url"],
            "farmer_id": farmer_id,
            "farmer_name": CATALOG_FARMER_NAME,
            "updated_at": now,
        }
        products.update_one(
            {"seed_key": item["seed_key"]},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True
        )
        seeded_count += 1

    print(f"[Seed] Successfully seeded {seeded_count} agricultural and grocery products!")

if __name__ == "__main__":
    run()
