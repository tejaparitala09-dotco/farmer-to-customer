import { useEffect, useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { ShoppingBasket } from 'lucide-react';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';

// Pages
import Home from './pages/Home';
import Products from './pages/Products';
import ProductDetails from './pages/ProductDetails';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import MyOrders from './pages/MyOrders';
import FarmerDashboard from './pages/FarmerDashboard';
import FarmerOrders from './pages/FarmerOrders';
import MyProducts from './pages/MyProducts';
import AddProduct from './pages/AddProduct';
import Login from './pages/Login';
import Register from './pages/Register';

import * as api from './api';

function useCart() {
  const [cart, setCart] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('ftc_cart') || '[]');
    } catch {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('ftc_cart', JSON.stringify(cart));
  }, [cart]);

  const add = (product, quantity = 1) => {
    setCart((prev) => {
      const existing = prev.find((item) => item.id === product.id);
      const available = Number(product.quantity) || 999;
      if (existing) {
        const nextQty = Math.min(existing.quantity + quantity, available);
        return prev.map((item) =>
          item.id === product.id ? { ...item, quantity: nextQty } : item
        );
      }
      return [
        ...prev,
        {
          ...product,
          quantity: Math.min(quantity, available),
          quantity_available: available,
        },
      ];
    });
  };

  const update = (id, quantity) => {
    if (quantity <= 0) {
      remove(id);
      return;
    }
    setCart((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, quantity } : item
      )
    );
  };

  const remove = (id) => {
    setCart((prev) => prev.filter((item) => item.id !== id));
  };

  const clear = () => {
    setCart([]);
  };

  return { cart, add, update, remove, clear };
}

export default function App() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loadingUser, setLoadingUser] = useState(true);
  const { cart, add, update, remove, clear } = useCart();

  useEffect(() => {
    const token = localStorage.getItem('ftc_token');
    if (token) {
      api.me()
        .then((userData) => {
          setUser(userData);
        })
        .catch(() => {
          localStorage.removeItem('ftc_token');
          setUser(null);
        })
        .finally(() => {
          setLoadingUser(false);
        });
    } else {
      setLoadingUser(false);
    }
  }, []);

  const logout = () => {
    localStorage.removeItem('ftc_token');
    setUser(null);
    navigate('/');
  };

  const totalCartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <>
      <Navbar user={user} logout={logout} cartCount={totalCartCount} />
      <Routes>
        {/* Public & Customer Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products add={add} />} />
        <Route path="/products/:id" element={<ProductDetails add={add} />} />
        <Route
          path="/cart"
          element={<Cart cart={cart} update={update} remove={remove} />}
        />
        <Route
          path="/checkout"
          element={
            <ProtectedRoute user={user} role="customer">
              <Checkout cart={cart} clear={clear} user={user} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/orders"
          element={
            <ProtectedRoute user={user} role="customer">
              <MyOrders />
            </ProtectedRoute>
          }
        />

        {/* Authentication Routes */}
        <Route path="/login" element={<Login setUser={setUser} />} />
        <Route path="/register" element={<Register setUser={setUser} />} />

        {/* Farmer Only Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute user={user} role="farmer">
              <FarmerDashboard user={user} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/my-products"
          element={
            <ProtectedRoute user={user} role="farmer">
              <MyProducts />
            </ProtectedRoute>
          }
        />
        <Route
          path="/add-product"
          element={
            <ProtectedRoute user={user} role="farmer">
              <AddProduct />
            </ProtectedRoute>
          }
        />
        <Route
          path="/farmer-orders"
          element={
            <ProtectedRoute user={user} role="farmer">
              <FarmerOrders />
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Home />} />
      </Routes>

      <footer>
        <span>
          <ShoppingBasket size={18} /> Farmer to Customer
        </span>
        <span>Fresh food. Direct journeys. Fair prices.</span>
      </footer>
    </>
  );
}
