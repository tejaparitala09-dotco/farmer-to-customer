import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ShoppingBasket } from 'lucide-react';
import Loading from '../components/Loading';
import * as api from '../api';

const trackingSteps = ['Pending', 'Confirmed', 'Packed', 'Out for Delivery', 'Delivered'];

export default function MyOrders() {
  const [orders, setOrders] = useState([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setBusy(true);
    api.myOrders()
      .then((data) => setOrders(data))
      .catch((err) => setError(err.message || 'Failed to load your orders'))
      .finally(() => setBusy(false));
  }, []);

  return (
    <main className="page section">
      <div className="page-intro">
        <span className="eyebrow">Your order history</span>
        <h1>Orders on their way.</h1>
        <p>Track your harvest deliveries from our farmers right to your doorstep.</p>
      </div>

      {error && <div className="notice error">{error}</div>}

      {busy ? (
        <Loading />
      ) : orders.length === 0 ? (
        <div className="empty">
          <ShoppingBasket size={48} style={{ color: '#9bb195', marginBottom: 12 }} />
          <h2>No orders placed yet.</h2>
          <p>Find something fresh from our local farmers today.</p>
          <Link className="button" to="/products" style={{ marginTop: 15 }}>
            Browse produce
          </Link>
        </div>
      ) : (
        <div className="orders">
          {orders.map((order) => {
            const currentStepIdx = trackingSteps.indexOf(order.status);
            const isCancelled = order.status === 'Cancelled';

            return (
              <article className="order-card" key={order.id}>
                <div className="order-top">
                  <div>
                    <span className="eyebrow">Order #{order.id.slice(-6).toUpperCase()}</span>
                    <p>
                      Placed on {new Date(order.created_at).toLocaleDateString(undefined, {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                      })}
                    </p>
                  </div>
                  <span className={`status ${order.status.toLowerCase().replace(/\s+/g, '-')}`}>
                    {order.status}
                  </span>
                </div>

                <div className="order-products">
                  {order.products.map((item, i) => (
                    <div key={i}>
                      <span>
                        {item.product_name} × {item.quantity} {item.unit || 'kg'}
                      </span>
                      <b>₹{(item.price * item.quantity).toFixed(2)}</b>
                    </div>
                  ))}
                </div>

                <div className="order-bottom">
                  <span>
                    Delivering to: {order.delivery_address?.city}, {order.delivery_address?.state} ({order.delivery_address?.pincode})
                  </span>
                  <strong>₹{Number(order.total_amount).toFixed(2)}</strong>
                </div>

                {!isCancelled && (
                  <div className="progress">
                    {trackingSteps.map((step, idx) => {
                      const isActive = currentStepIdx >= idx;
                      return (
                        <div className={isActive ? 'active' : ''} key={step}>
                          <i></i>
                          <span>{step}</span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </article>
            );
          })}
        </div>
      )}
    </main>
  );
}
