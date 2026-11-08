const BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
async function request(path, options = {}) { const token = localStorage.getItem('ftc_token'); const response = await fetch(`${BASE}${path}`, { ...options, headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(options.headers || {}) } }); const data = await response.json().catch(() => ({})); if (!response.ok) throw new Error(data.detail || 'Something went wrong'); return data; }
const body = data => ({ method: 'POST', body: JSON.stringify(data) });
export const register = data => request('/api/auth/register', body(data));
export const login = data => request('/api/auth/login', body(data));
export const me = () => request('/api/auth/me');
export const getProducts = (search = '', category = '') => request(`/api/products?search=${encodeURIComponent(search)}&category=${encodeURIComponent(category)}`);
export const getProduct = id => request(`/api/products/${id}`);
export const myProducts = () => request('/api/products/farmer/mine');
export const addProduct = data => request('/api/products', body(data));
export const editProduct = (id, data) => request(`/api/products/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteProduct = id => request(`/api/products/${id}`, { method: 'DELETE' });
export const createOrder = data => request('/api/orders', body(data));
export const myOrders = () => request('/api/orders/my-orders');
export const farmerOrders = () => request('/api/orders/farmer-orders');
export const updateOrderStatus = (id, status) => request(`/api/orders/${id}/status`, { method: 'PUT', body: JSON.stringify({ status }) });
