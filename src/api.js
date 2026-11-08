import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (import.meta.env.PROD ? '' : 'http://localhost:8000');
const TOKEN_KEY = 'ftc_access_token';
const USER_KEY = 'ftc_user';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  register(role, payload) {
    return apiClient.post(`/api/auth/register/${role}`, payload);
  },
  login(payload) {
    return apiClient.post('/api/auth/login', payload);
  },
  getCurrentUser() {
    return apiClient.get('/api/users/me');
  },
};

export const productApi = {
  list(params = {}) {
    return apiClient.get('/api/products', { params });
  },
  get(productId) {
    return apiClient.get(`/api/products/${productId}`);
  },
  mine() {
    return apiClient.get('/api/farmer/products');
  },
  create(payload) {
    return apiClient.post('/api/products', payload);
  },
  update(productId, payload) {
    return apiClient.put(`/api/products/${productId}`, payload);
  },
  remove(productId) {
    return apiClient.delete(`/api/products/${productId}`);
  },
};

export const orderApi = {
  create(payload) {
    return apiClient.post('/api/orders', payload);
  },
  mine() {
    return apiClient.get('/api/orders/my');
  },
  farmerOrders() {
    return apiClient.get('/api/farmer/orders');
  },
  updateStatus(orderId, status) {
    return apiClient.put(`/api/farmer/orders/${orderId}/status`, { status });
  },
};

export const authStorage = {
  save(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },
  getUser() {
    const storedUser = localStorage.getItem(USER_KEY);
    if (!storedUser) return null;

    try {
      return JSON.parse(storedUser);
    } catch {
      localStorage.removeItem(USER_KEY);
      return null;
    }
  },
  clear() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },
};

export function getApiErrorMessage(error) {
  const detail = error.response?.data?.detail;
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg).join(' ');
  }
  if (typeof detail === 'string') return detail;
  if (error.request) return 'The server is unavailable. Please try again shortly.';
  return 'Something went wrong. Please try again.';
}
