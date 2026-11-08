const rawBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const BASE = rawBase.replace(/\/+$/, '');

async function request(path, options = {}) {
  const token = localStorage.getItem('ftc_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const url = `${BASE}${path.startsWith('/') ? path : `/${path}`}`;
  let response;
  try {
    response = await fetch(url, { ...options, headers });
  } catch (err) {
    throw new Error('Unable to connect to the server. Please check your network connection.');
  }

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    let message = 'Something went wrong';
    if (typeof data.detail === 'string') {
      message = data.detail;
    } else if (Array.isArray(data.detail)) {
      message = data.detail.map((d) => d.msg || `${d.loc?.slice(-1)[0]} is invalid`).join(', ');
    } else if (data.message) {
      message = data.message;
    }
    throw new Error(message);
  }
  return data;
}

const post = (data) => ({ method: 'POST', body: JSON.stringify(data) });
const put = (data) => ({ method: 'PUT', body: JSON.stringify(data) });

// Authentication
export const register = (data) => request('/api/auth/register', post(data));
export const login = (data) => request('/api/auth/login', post(data));
export const me = () => request('/api/auth/me');

// Products
export const getProducts = (search = '', category = '') =>
  request(`/api/products?search=${encodeURIComponent(search)}&category=${encodeURIComponent(category)}`);
export const getProduct = (id) => request(`/api/products/${id}`);
export const myProducts = () => request('/api/products/farmer/mine');
export const addProduct = (data) => request('/api/products', post(data));
export const editProduct = (id, data) => request(`/api/products/${id}`, put(data));
export const deleteProduct = (id) => request(`/api/products/${id}`, { method: 'DELETE' });

// Orders
export const createOrder = (data) => request('/api/orders', post(data));
export const myOrders = () => request('/api/orders/my-orders');
export const farmerOrders = () => request('/api/orders/farmer-orders');
export const updateOrderStatus = (id, status) => request(`/api/orders/${id}/status`, put({ status }));
