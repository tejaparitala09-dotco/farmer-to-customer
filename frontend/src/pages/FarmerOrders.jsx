import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Loading from '../components/Loading';
import * as api from '../api';

const statusOptions = ['Pending', 'Confirmed', 'Packed', 'Out for Delivery', 'Delivered', 'Cancelled'];

export default function FarmerOrders() {
  const [orders, setOrders] = useState([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const loadOrders = () => {
    setBusy(true);
    setError('');
    api.farmerOrders()
      .then((data) => setOrders(data))
      .catch((err) => setError(err.message || 'Failed to load farmer orders'))
      .finally(() => setBusy(false));
  };

  useEffect(() => {
    loadOrders();
  }, []);

  const handleStatusChange = async (orderId, newStatus) => {
    try {
      await api.updateOrderStatus(orderId, newStatus);
      setOrders((prev) =>
        prev.map((o) => (o.id === orderId ? { ...o, status: newStatus } : o))
      );
      setSuccess(`Order #${orderId.slice(-6).toUpperCase()} updated to '${newStatus}'`);
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to update order status');
    }
  };

  return (
    <main className="page section">
      <div className="page-intro">
        <span className="eyebrow">Order Fulfillment</span>
        <h1>Orders to prepare.</h1>
        <p>Update delivery progress as you harvest, pack, and hand over produce for transit.</p>
      </div>

      {error && <div className="notice error">{error}</div>}
      {success && <div className="notice">{success}</div>}

      {busy ? (
        <Loading />
      ) : orders.length === 0 ? (
        <div className="empty">
          <h2>No orders received yet.</h2>
          <p>Orders placed by customers for your produce will appear here.</p>
        </div>
      ) : (
        <div className="orders">
          {orders.map((order) => (
            <article className="order-card" key={order.id}>
              <div className="order-top">
                <div>
                  <span className="eyebrow">Order #{order.id.slice(-6).toUpperCase()}</span>
                  <p>
                    <strong>Customer:</strong> {order.customer?.name || 'Customer'}
                    {order.customer?.phone && ` · 📞 ${order.customer.phone}`}
                  </p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span style={{ fontSize: 13, color: 'var(--muted)' }}>Status:</span>
                  <select
                    value={order.status}
                    onChange={(e) => handleStatusChange(order.id, e.target.value)}
                    style={{ fontWeight: 600 }}
                  >
                    {statusOptions.map((opt) => (
                      <option key={opt} value={opt}>
                        {opt}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="order-products">
                {order.products.map((p, idx) => (
                  <div key={idx}>
                    <span>
                      {p.product_name} × {p.quantity} {p.unit || 'kg'}
                    </span>
                    <b>₹{(p.price * p.quantity).toFixed(2)}</b>
                  </div>
                ))}
              </div>

              <div className="order-bottom">
                <span>
                  Delivery Address: {order.delivery_address?.address}, {order.delivery_address?.city}, {order.delivery_address?.state} - {order.delivery_address?.pincode}
                </span>
                <strong>Total: ₹{Number(order.total_amount).toFixed(2)}</strong>
              </div>
            </article>
          ))}
        </div>
      )}
    </main>
  );
}
