import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, ShoppingBasket, Truck } from 'lucide-react';
import Loading from '../components/Loading';
import * as api from '../api';

export default function FarmerDashboard({ user }) {
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setBusy(true);
    Promise.all([api.myProducts(), api.farmerOrders()])
      .then(([prods, ords]) => {
        setProducts(prods || []);
        setOrders(ords || []);
      })
      .catch((err) => setError(err.message || 'Failed to load dashboard data'))
      .finally(() => setBusy(false));
  }, []);

  const stats = [
    { label: 'Total Products', count: products.length },
    { label: 'Pending', count: orders.filter((o) => o.status === 'Pending').length },
    { label: 'Confirmed', count: orders.filter((o) => o.status === 'Confirmed').length },
    { label: 'Packed', count: orders.filter((o) => o.status === 'Packed').length },
    { label: 'Out for Delivery', count: orders.filter((o) => o.status === 'Out for Delivery').length },
    { label: 'Delivered', count: orders.filter((o) => o.status === 'Delivered').length },
  ];

  if (busy) return <Loading />;

  return (
    <main className="page section">
      <div className="page-intro">
        <span className="eyebrow">Farmer Workspace</span>
        <h1>Welcome, {user?.name || 'Farmer'}. <em>Your harvest in view.</em></h1>
        <p>Monitor your published produce inventory and fulfill customer orders in real time.</p>
      </div>

      {error && <div className="notice error">{error}</div>}

      <div className="stats">
        {stats.map((s) => (
          <div className="stat" key={s.label}>
            <span>{s.label}</span>
            <b>{s.count}</b>
          </div>
        ))}
      </div>

      <div className="quick">
        <Link to="/add-product" className="feature peach">
          <Plus size={32} />
          <h3>Add a product</h3>
          <p>Publish fresh crops, fruits, or dairy directly to the consumer marketplace.</p>
        </Link>
        <Link to="/my-products" className="feature green">
          <ShoppingBasket size={32} />
          <h3>Manage products</h3>
          <p>Review current inventory, update stock levels, and remove inactive produce.</p>
        </Link>
        <Link to="/farmer-orders" className="feature cream">
          <Truck size={32} />
          <h3>Manage orders</h3>
          <p>Prepare harvests, change fulfillment status, and track doorstep deliveries.</p>
        </Link>
      </div>
    </main>
  );
}
