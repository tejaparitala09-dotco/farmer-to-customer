import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes.auth_routes import router as auth_router
from routes.product_routes import router as product_router
from routes.order_routes import router as order_router

app = FastAPI(title="Farmer to Customer API")
origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").replace("[", "").replace("]", "").split(",")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in origins], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router); app.include_router(product_router); app.include_router(order_router)
@app.on_event("startup")
def startup(): init_db()
@app.get("/")
def root(): return {"message":"Farmer to Customer API is running"}
