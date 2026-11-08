from datetime import datetime, timezone
from database import users, products, init_db
from auth import hash_password

items = [
("Tomato","Vegetables",40,"kg"),("Potato","Vegetables",35,"kg"),("Onion","Vegetables",45,"kg"),("Carrot","Vegetables",50,"kg"),("Brinjal","Vegetables",40,"kg"),("Cabbage","Vegetables",30,"kg"),("Cauliflower","Vegetables",45,"kg"),("Spinach","Vegetables",25,"bunch"),("Green Chilli","Vegetables",80,"kg"),("Capsicum","Vegetables",70,"kg"),("Cucumber","Vegetables",40,"kg"),("Bitter Gourd","Vegetables",60,"kg"),("Bottle Gourd","Vegetables",35,"piece"),("Ridge Gourd","Vegetables",50,"kg"),("Drumstick","Vegetables",80,"kg"),("Lady Finger","Vegetables",55,"kg"),("Beetroot","Vegetables",50,"kg"),("Radish","Vegetables",35,"kg"),("Pumpkin","Vegetables",30,"kg"),("Green Peas","Vegetables",90,"kg"),
("Apple","Fruits",120,"kg"),("Banana","Fruits",60,"dozen"),("Mango","Fruits",100,"kg"),("Orange","Fruits",80,"kg"),("Papaya","Fruits",50,"kg"),("Guava","Fruits",70,"kg"),("Grapes","Fruits",100,"kg"),("Pomegranate","Fruits",140,"kg"),("Watermelon","Fruits",40,"kg"),("Pineapple","Fruits",70,"piece"),("Lemon","Fruits",80,"kg"),("Sapota","Fruits",80,"kg"),("Jackfruit","Fruits",60,"kg"),("Custard Apple","Fruits",100,"kg"),("Muskmelon","Fruits",60,"kg"),
("Rice","Grains",70,"kg"),("Wheat","Grains",55,"kg"),("Maize","Grains",40,"kg"),("Ragi","Millets",60,"kg"),("Jowar","Millets",50,"kg"),("Bajra","Millets",45,"kg"),("Foxtail Millet","Millets",90,"kg"),("Little Millet","Millets",100,"kg"),
("Green Gram","Pulses",110,"kg"),("Black Gram","Pulses",120,"kg"),("Red Gram","Pulses",130,"kg"),("Chickpeas","Pulses",100,"kg"),("Turmeric","Spices",160,"kg"),("Ginger","Spices",100,"kg"),("Garlic","Spices",140,"kg")]

images = {"Vegetables":"https://images.unsplash.com/photo-1540420773420-3366772f4999?w=900", "Fruits":"https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=900", "Grains":"https://images.unsplash.com/photo-1586201375761-83865001e31c?w=900", "Millets":"https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=900", "Pulses":"https://images.unsplash.com/photo-1515543904379-3d757afe72e4?w=900", "Spices":"https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=900"}

def run():
    init_db()
    farmer = users.find_one({"email":"seed.farmer@example.com"})
    if not farmer:
        farmer = {"name":"Green Valley Farm","email":"seed.farmer@example.com","password_hash":hash_password("Farmer@123"),"phone":"9000000000","role":"farmer"}
        farmer["_id"] = users.insert_one(farmer).inserted_id
    for index, (name, category, price, unit) in enumerate(items):
        products.update_one({"seed_key": name.lower()}, {"$setOnInsert": {"seed_key":name.lower(),"product_name":name,"category":category,"price":price,"unit":unit,"quantity":[20,30,50,75,100][index%5],"description":f"Fresh, carefully harvested {name.lower()} sourced from Green Valley Farm.","image_url":images[category],"farmer_id":farmer["_id"],"created_at":datetime.now(timezone.utc)}}, upsert=True)
    print(f"Seeded {len(items)} products. Farmer login: seed.farmer@example.com / Farmer@123")

if __name__ == "__main__": run()
