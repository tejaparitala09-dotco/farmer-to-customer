"""Fast and direct unit & integration tests for Farmer to Customer backend.
Directly tests:
- Models & Pydantic validation
- Auth & bcrypt password hashing
- JWT generation & verification
- Route handlers (auth, products, orders)
- Role verification & security logic
"""
import sys
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from datetime import datetime, timezone
from fastapi import HTTPException

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import auth
import models
from routes import auth_routes, product_routes, order_routes

class TestFarmerToCustomerBackend(unittest.TestCase):
    def test_01_models_validation(self):
        # Valid register
        reg = models.RegisterRequest(
            name="Ramesh Kumar",
            email="ramesh@example.com",
            password="securepassword123",
            phone="+91 9876543210",
            role="farmer"
        )
        self.assertEqual(reg.role, "farmer")

        # Invalid role raises ValueError
        with self.assertRaises(ValueError):
            models.RegisterRequest(
                name="Ramesh",
                email="ramesh@example.com",
                password="password",
                role="invalid_role"
            )

        # Valid product
        prod = models.ProductRequest(
            product_name="Himalayan Apples",
            category="Fruits",
            price=120.0,
            unit="kg",
            quantity=50.0,
            description="Crisp organic apples straight from orchard."
        )
        self.assertEqual(prod.price, 120.0)
        self.assertEqual(prod.unit, "kg")

    def test_02_password_hashing_and_jwt(self):
        plain = "MySecretPass@123"
        hashed = auth.hash_password(plain)
        self.assertNotEqual(plain, hashed)
        self.assertTrue(auth.verify_password(plain, hashed))
        self.assertFalse(auth.verify_password("WrongPassword", hashed))

        # Test JWT token generation and validation
        user_id = ObjectId()
        user_doc = {
            "_id": user_id,
            "name": "Test Farmer",
            "email": "farmer@test.com",
            "role": "farmer"
        }
        token = auth.create_token(user_doc)
        self.assertIsInstance(token, str)

        import jwt
        decoded = jwt.decode(token, auth.SECRET, algorithms=["HS256"])
        self.assertEqual(decoded["sub"], str(user_id))
        self.assertEqual(decoded["role"], "farmer")

    @patch("routes.auth_routes.users")
    def test_03_auth_register_and_login_routes(self, mock_users):
        mock_users.find_one.return_value = None
        new_id = ObjectId()
        mock_users.insert_one.return_value = MagicMock(inserted_id=new_id)

        reg_payload = models.RegisterRequest(
            name="Anita Roy",
            email="anita@example.com",
            password="Password123",
            phone="9876543210",
            role="customer"
        )
        res = auth_routes.register(reg_payload)
        self.assertIn("token", res)
        self.assertEqual(res["user"]["email"], "anita@example.com")
        self.assertEqual(res["user"]["role"], "customer")

        # Login existing customer
        hashed = auth.hash_password("Password123")
        mock_users.find_one.return_value = {
            "_id": new_id,
            "name": "Anita Roy",
            "email": "anita@example.com",
            "password_hash": hashed,
            "phone": "9876543210",
            "role": "customer"
        }
        login_res = auth_routes.login(models.LoginRequest(
            email="anita@example.com",
            password="Password123"
        ))
        self.assertIn("token", login_res)
        self.assertEqual(login_res["user"]["role"], "customer")

        # Bad password raises 401
        with self.assertRaises(HTTPException) as ctx:
            auth_routes.login(models.LoginRequest(
                email="anita@example.com",
                password="WrongPassword"
            ))
        self.assertEqual(ctx.exception.status_code, 401)

    @patch("routes.product_routes.products")
    def test_04_product_routes(self, mock_products):
        farmer_id = ObjectId()
        farmer = {"id": str(farmer_id), "name": "Green Farm", "role": "farmer"}

        # Add product
        mock_products.insert_one.return_value = MagicMock(inserted_id=ObjectId())
        new_prod = models.ProductRequest(
            product_name="Organic Tomatoes",
            category="Vegetables",
            price=40.0,
            unit="kg",
            quantity=100.0,
            description="Fresh vine-ripened tomatoes"
        )
        created = product_routes.add_product(new_prod, farmer=farmer)
        self.assertEqual(created["product_name"], "Organic Tomatoes")
        self.assertEqual(created["farmer_id"], str(farmer_id))

        # List products
        mock_cursor = MagicMock()
        mock_cursor.sort.return_value = [created]
        mock_products.find.return_value = mock_cursor

        listed = product_routes.list_products(search="Tomatoes", category="Vegetables")
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]["product_name"], "Organic Tomatoes")

    @patch("routes.order_routes.products")
    @patch("routes.order_routes.orders")
    def test_05_order_routes(self, mock_orders, mock_products):
        prod_id = ObjectId()
        farmer_id = ObjectId()
        customer_id = ObjectId()

        mock_products.find_one.return_value = {
            "_id": prod_id,
            "product_name": "Organic Tomatoes",
            "price": 40.0,
            "unit": "kg",
            "quantity": 100.0,
            "farmer_id": farmer_id
        }
        order_id = ObjectId()
        mock_orders.insert_one.return_value = MagicMock(inserted_id=order_id)

        customer = {"id": str(customer_id), "name": "Customer Priya", "role": "customer"}
        order_req = models.CreateOrderRequest(
            items=[models.OrderItem(product_id=str(prod_id), quantity=2.0)],
            delivery_address=models.Address(
                full_name="Priya Sharma",
                phone="9876543210",
                address="123 Farm Way",
                city="Bengaluru",
                state="Karnataka",
                pincode="560001"
            )
        )

        res = order_routes.create_order(order_req, customer=customer)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["total_amount"], 80.0)
        self.assertEqual(res[0]["status"], "Pending")

        # Farmer status update
        farmer = {"id": str(farmer_id), "name": "Green Farm", "role": "farmer"}
        mock_orders.find_one.return_value = {
            "_id": order_id,
            "farmer_id": farmer_id,
            "status": "Pending"
        }
        update_res = order_routes.update_status(
            str(order_id),
            models.StatusRequest(status="Confirmed"),
            farmer=farmer
        )
        self.assertEqual(update_res["status"], "Confirmed")

if __name__ == "__main__":
    unittest.main()
