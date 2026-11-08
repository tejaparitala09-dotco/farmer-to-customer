# Farmer to Customer

A full-stack agricultural marketplace connecting local farmers and customers. The frontend is React/Vite; the API is FastAPI/PyMongo; authentication uses bcrypt and JWT; data is stored in MongoDB.

## Run locally

### 1. Start MongoDB

Run MongoDB locally on its default port, or set `MONGODB_URI` to a hosted MongoDB connection string.

### 2. Start the API

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python seed_products.py
uvicorn main:app --reload --port 8000
```

The seed command is safe to run repeatedly. It creates 50 products and the sample farmer account:

- Email: `seed.farmer@example.com`
- Password: `Farmer@123`

### 3. Start the frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. To use another API URL, set `VITE_API_BASE_URL` before starting Vite.

## API overview

- `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`
- `GET /api/products`, `GET /api/products/{id}`
- Farmer-only product create, edit, delete, and `/api/products/farmer/mine`
- `POST /api/orders`, `GET /api/orders/my-orders`
- Farmer-only `GET /api/orders/farmer-orders` and `PUT /api/orders/{id}/status`

Orders are grouped by farmer at checkout, so one customer cart can correctly produce multiple farmer orders. Product ownership and order access are enforced by the API, not only the UI.

## Environment

See `backend/.env.example` for MongoDB, JWT, and frontend origin settings. Secrets remain backend-only.
