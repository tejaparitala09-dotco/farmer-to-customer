"""Farmer to Customer API."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4
import os
import re

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

try:
    from .database import (
        PyMongoError,
        check_connection,
        ensure_indexes,
        find_user_by_email,
        get_collection,
        orders_collection,
        products_collection,
    )
    from .models import (
        CustomerDocument,
        FarmerDocument,
        LoginRequest,
        OrderCreate,
        OrderResponse,
        OrderStatusUpdate,
        ProductCategory,
        ProductCreate,
        ProductResponse,
        RegistrationRequest,
        TokenResponse,
        UserResponse,
        UserRole,
    )
except ImportError:
    from database import (
        PyMongoError,
        check_connection,
        ensure_indexes,
        find_user_by_email,
        get_collection,
        orders_collection,
        products_collection,
    )
    from models import (
        CustomerDocument,
        FarmerDocument,
        LoginRequest,
        OrderCreate,
        OrderResponse,
        OrderStatusUpdate,
        ProductCategory,
        ProductCreate,
        ProductResponse,
        RegistrationRequest,
        TokenResponse,
        UserResponse,
        UserRole,
    )

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-development-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

configured_origins = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000",
)
allowed_origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()]

app = FastAPI(
    title="Farmer to Customer API",
    version="0.1.0",
    description="Starter API for customer and farmer accounts.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def user_response(user: dict) -> UserResponse:
    return UserResponse(
        id=user["id"],
        full_name=user["full_name"],
        email=user["email"],
        phone_number=user["phone_number"],
        role=user["role"],
    )


def create_access_token(email: str, role: UserRole) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "role": role, "exp": expires_at}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def register_user(payload: RegistrationRequest, role: UserRole) -> UserResponse:
    email = str(payload.email).lower()
    try:
        check_connection()
        ensure_indexes()
        if find_user_by_email(email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        document_model = CustomerDocument if role == "customer" else FarmerDocument
        user = document_model(
            id=str(uuid4()),
            full_name=payload.full_name.strip(),
            email=email,
            phone_number=payload.phone_number.strip(),
            password_hash=password_context.hash(payload.password),
        ).model_dump()
        get_collection(role).insert_one(user)
    except DuplicateKeyError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        ) from error
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error
    return user_response(user)


@app.get("/api/health")
def health_check() -> dict:
    try:
        check_connection()
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable.",
        ) from error
    return {"status": "ok", "service": "farmer-to-customer-api", "database": "connected"}


@app.post(
    "/api/auth/register/customer",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_customer(payload: RegistrationRequest) -> UserResponse:
    return register_user(payload, "customer")


@app.post(
    "/api/auth/register/farmer",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_farmer(payload: RegistrationRequest) -> UserResponse:
    return register_user(payload, "farmer")


@app.post("/api/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    email = str(payload.email).lower()
    try:
        check_connection()
        user = find_user_by_email(email)
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error

    if user is None or not password_context.verify(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(
        access_token=create_access_token(email, user["role"]),
        token_type="bearer",
        user=user_response(user),
    )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        if not isinstance(email, str) or role not in ("customer", "farmer"):
            raise credentials_exception
    except JWTError as error:
        raise credentials_exception from error

    try:
        check_connection()
        user = get_collection(role).find_one({"email": email})
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error
    if user is None:
        raise credentials_exception
    return user


@app.get("/api/users/me", response_model=UserResponse)
async def get_my_profile(current_user: dict = Depends(get_current_user)) -> UserResponse:
    return user_response(current_user)


def require_role(required_role: UserRole):
    async def role_dependency(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Only {required_role}s can access this resource.",
            )
        return current_user

    return role_dependency


require_customer = require_role("customer")
require_farmer = require_role("farmer")


def product_response(product: dict) -> ProductResponse:
    return ProductResponse.model_validate(product)


def order_response(order: dict) -> OrderResponse:
    return OrderResponse.model_validate(order)


@app.get("/api/products", response_model=list[ProductResponse])
def list_products(
    search: str | None = Query(default=None, min_length=1, max_length=100),
    category: ProductCategory | None = None,
) -> list[ProductResponse]:
    filters: dict = {}
    if search:
        filters["product_name"] = {"$regex": re.escape(search.strip()), "$options": "i"}
    if category:
        filters["category"] = category

    try:
        check_connection()
        products = products_collection.find(filters).sort("created_at", -1)
        return [product_response(product) for product in products]
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error


@app.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: str) -> ProductResponse:
    try:
        check_connection()
        product = products_collection.find_one({"id": product_id})
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return product_response(product)


@app.post("/api/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, farmer: dict = Depends(require_farmer)) -> ProductResponse:
    now = datetime.now(timezone.utc)
    product = payload.model_dump()
    product.update(
        {
            "id": str(uuid4()),
            "farmer_id": farmer["id"],
            "farmer_name": farmer["full_name"],
            "created_at": now,
            "updated_at": now,
        }
    )
    try:
        ensure_indexes()
        products_collection.insert_one(product)
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error
    return product_response(product)


@app.get("/api/farmer/products", response_model=list[ProductResponse])
def list_farmer_products(farmer: dict = Depends(require_farmer)) -> list[ProductResponse]:
    try:
        products = products_collection.find({"farmer_id": farmer["id"]}).sort("created_at", -1)
        return [product_response(product) for product in products]
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error


@app.put("/api/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    payload: ProductCreate,
    farmer: dict = Depends(require_farmer),
) -> ProductResponse:
    update = payload.model_dump()
    update["updated_at"] = datetime.now(timezone.utc)
    try:
        result = products_collection.update_one(
            {"id": product_id, "farmer_id": farmer["id"]},
            {"$set": update},
        )
        if result.matched_count == 0:
            exists = products_collection.find_one({"id": product_id})
            if exists is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your own products.")
        product = products_collection.find_one({"id": product_id})
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error
    return product_response(product)


@app.delete("/api/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, farmer: dict = Depends(require_farmer)) -> None:
    try:
        result = products_collection.delete_one({"id": product_id, "farmer_id": farmer["id"]})
        if result.deleted_count == 0:
            exists = products_collection.find_one({"id": product_id})
            if exists is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own products.")
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error


@app.post("/api/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, customer: dict = Depends(require_customer)) -> OrderResponse:
    requested_quantities: dict[str, float] = {}
    for item in payload.items:
        requested_quantities[item.product_id] = requested_quantities.get(item.product_id, 0) + item.quantity

    try:
        ensure_indexes()
        order_items = []
        farmer_ids = set()
        total_amount = 0.0
        for product_id, quantity in requested_quantities.items():
            product = products_collection.find_one({"id": product_id})
            if product is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found.")
            if quantity > product["quantity"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Only {product['quantity']} {product['unit']} available for {product['product_name']}.",
                )
            line_total = round(product["price"] * quantity, 2)
            total_amount += line_total
            farmer_ids.add(product["farmer_id"])
            order_items.append(
                {
                    "product_id": product["id"],
                    "farmer_id": product["farmer_id"],
                    "farmer_name": product["farmer_name"],
                    "product_name": product["product_name"],
                    "unit": product["unit"],
                    "price": product["price"],
                    "quantity": quantity,
                    "line_total": line_total,
                }
            )
        now = datetime.now(timezone.utc)
        order = {
            "id": str(uuid4()),
            "customer_id": customer["id"],
            "customer_name": customer["full_name"],
            "farmer_ids": list(farmer_ids),
            "items": order_items,
            "total_amount": round(total_amount, 2),
            "delivery_address": payload.delivery_address.strip(),
            "status": "Pending",
            "created_at": now,
            "updated_at": now,
        }
        orders_collection.insert_one(order)
        return order_response(order)
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error


@app.get("/api/orders/my", response_model=list[OrderResponse])
def list_customer_orders(customer: dict = Depends(require_customer)) -> list[OrderResponse]:
    try:
        orders = orders_collection.find({"customer_id": customer["id"]}).sort("created_at", -1)
        return [order_response(order) for order in orders]
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error


@app.get("/api/farmer/orders", response_model=list[OrderResponse])
def list_farmer_orders(farmer: dict = Depends(require_farmer)) -> list[OrderResponse]:
    try:
        orders = orders_collection.find({"farmer_ids": farmer["id"]}).sort("created_at", -1)
        return [order_response(order) for order in orders]
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error


@app.put("/api/farmer/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: str,
    payload: OrderStatusUpdate,
    farmer: dict = Depends(require_farmer),
) -> OrderResponse:
    try:
        order = orders_collection.find_one({"id": order_id})
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
        if farmer["id"] not in order.get("farmer_ids", []):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This order is not related to your products.")

        allowed_next_statuses = {
            "Pending": {"Confirmed", "Cancelled"},
            "Confirmed": {"Shipped", "Cancelled"},
            "Shipped": {"Out for Delivery", "Cancelled"},
            "Out for Delivery": {"Delivered"},
            "Delivered": set(),
            "Cancelled": set(),
            "Preparing": {"Shipped", "Cancelled"},
        }
        current_status = order["status"]
        if payload.status != current_status and payload.status not in allowed_next_statuses.get(current_status, set()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Order status can move from {current_status} to the next step only.",
            )

        orders_collection.update_one(
            {"id": order_id, "farmer_ids": farmer["id"]},
            {"$set": {"status": payload.status, "updated_at": datetime.now(timezone.utc)}},
        )
        return order_response(orders_collection.find_one({"id": order_id}))
    except PyMongoError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable. Please try again later.",
        ) from error
