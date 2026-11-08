# Farmer to Customer 🌾🛒

A full-stack direct-to-consumer agricultural marketplace connecting local farmers and household customers.
- **Frontend**: React (Vite, React Router DOM, Lucide Icons)
- **Backend**: Python FastAPI, PyMongo, Pydantic v2
- **Database**: MongoDB Atlas / MongoDB
- **Security**: bcrypt password hashing & HS256 JWT Authentication

---

## Architecture & Features

### 1. Role-Based Authentication
- **Customer**: Browse seasonal produce, filter & search, manage cart, place orders with delivery address, track order journey in real-time.
- **Farmer**: Dedicated dashboard with harvest metrics, catalog management (add, view, edit, delete produce), and order fulfillment workflow (Pending ➔ Confirmed ➔ Packed ➔ Out for Delivery ➔ Delivered).

### 2. Built-in Sample Catalog
The database includes 28+ agricultural items across Vegetables, Fruits, Grains, Millets, Pulses, Spices, and Grocery:
- **Default Farmer Account**: `farmer@farm.com` / `Password@123` (or `seed.farmer@example.com` / `Farmer@123`)
- **Default Customer Account**: `customer@fresh.com` / `Password@123`

---

## Local Development

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MongoDB Atlas or local MongoDB URI
python seed_products.py
uvicorn main:app --reload --port 8000
```
Backend API documentation is available at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173`.

---

## Deployment Guide

### Part A: Backend Deployment to Render (FastAPI)

1. Sign in to [Render](https://render.com) and click **New +** ➔ **Web Service**.
2. Connect your GitHub repository: `https://github.com/tejaparitala09-dotco/farmer-to-customer`.
3. Configure the service settings:
   - **Name**: `farmer-to-customer-api`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. In the **Environment Variables** section, add:
   | Key | Value | Description |
   | --- | --- | --- |
   | `MONGODB_URI` | `mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority` | Your MongoDB Atlas connection URI |
   | `MONGODB_DATABASE` | `farmer_to_customer` | Target database name |
   | `JWT_SECRET_KEY` | *(generate a secure random 32+ char string)* | Secret for signing auth tokens |
   | `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token expiration time (e.g. 24 hours) |
   | `FRONTEND_ORIGINS` | `https://your-app.vercel.app,http://localhost:5173` | Allowed origins for CORS |
   | `PYTHON_VERSION` | `3.11.9` | Stable Python runtime version |
5. Click **Create Web Service**.
6. Once deployed, note your Render service URL (e.g., `https://farmer-to-customer-api.onrender.com`).
7. *(Optional)* Run product seeding in Render Shell:
   ```bash
   python seed_products.py
   ```

### Part B: MongoDB Atlas Configuration
1. In [MongoDB Atlas](https://cloud.mongodb.com):
   - Go to **Network Access** ➔ Add IP Address ➔ Select **Allow Access From Anywhere (`0.0.0.0/0`)** so Render can connect.
   - Go to **Database Access** ➔ Create a database user with Read/Write privileges.
   - Go to **Database** ➔ Click **Connect** ➔ **Drivers** (Python 3.11+) and copy the connection string.

### Part C: Frontend Deployment to Vercel (React)

1. Sign in to [Vercel](https://vercel.com) and click **Add New...** ➔ **Project**.
2. Import the `farmer-to-customer` GitHub repository.
3. In **Project Settings**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click edit and select `frontend` (or leave default root, both are supported).
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. In **Environment Variables**, add:
   | Key | Value |
   | --- | --- |
   | `VITE_API_BASE_URL` | `https://farmer-to-customer-api.onrender.com` |
   *(Replace with your actual Render API URL from Part A)*
5. Click **Deploy**.
6. Once deployed, copy your Vercel URL and add it to `FRONTEND_ORIGINS` in your Render Web Service.

---

## Verification & Testing
- Run test suite: `python backend/test_backend.py`
- Test frontend build: `npm run build`
- API Health Check: `GET /health` and `GET /`
