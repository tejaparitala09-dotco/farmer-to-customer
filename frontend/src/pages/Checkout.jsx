import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Check, ArrowRight } from 'lucide-react';
import * as api from '../api';

export default function Checkout({ cart, clear, user }) {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    full_name: user?.name || '',
    phone: user?.phone || '',
    address: '',
    city: '',
    state: '',
    pincode: '',
  });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (cart.length === 0) {
      navigate('/products');
    }
  }, [cart, navigate]);

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    setError('');

    // Client-side validations matching backend schema
    if (!form.full_name.trim() || form.full_name.length < 2) {
      setError('Please provide your full recipient name (at least 2 letters).');
      return;
    }
    if (!form.phone.trim() || form.phone.length < 6) {
      setError('Please provide a valid contact phone number.');
      return;
    }
    if (!form.address.trim() || form.address.length < 3) {
      setError('Please provide a complete street address.');
      return;
    }
    if (!form.city.trim() || form.city.length < 2) {
      setError('Please provide a city name.');
      return;
    }
    if (!form.state.trim() || form.state.length < 2) {
      setError('Please provide a state name.');
      return;
    }
    if (!form.pincode.trim() || form.pincode.length < 3) {
      setError('Please provide a valid delivery pincode / postal code.');
      return;
    }

    setSubmitting(true);
    try {
      const orderPayload = {
        items: cart.map((x) => ({
          product_id: x.id,
          quantity: x.quantity,
        })),
        delivery_address: {
          full_name: form.full_name.trim(),
          phone: form.phone.trim(),
          address: form.address.trim(),
          city: form.city.trim(),
          state: form.state.trim(),
          pincode: form.pincode.trim(),
        },
      };

      await api.createOrder(orderPayload);
      clear();
      navigate('/orders');
    } catch (err) {
      setError(err.message || 'Failed to place order. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="page section narrow">
      <Link className="back" to="/cart">← Back to basket</Link>
      <div className="page-intro">
        <span className="eyebrow">Almost there</span>
        <h1>Delivery <em>details.</em></h1>
        <p>Confirm where our farmers should deliver your fresh produce.</p>
      </div>

      {error && <div className="notice error">{error}</div>}

      <div className="checkout-grid">
        <form className="form-card" onSubmit={handleSubmit}>
          <label className="field">
            <span>Full Name</span>
            <input
              required
              placeholder="e.g. Priya Sharma"
              value={form.full_name}
              onChange={(e) => setForm({ ...form, full_name: e.target.value })}
            />
          </label>
          <label className="field">
            <span>Phone Number</span>
            <input
              required
              type="tel"
              placeholder="e.g. +91 9876543210"
              value={form.phone}
              onChange={(e) => setForm({ ...form, phone: e.target.value })}
            />
          </label>
          <label className="field">
            <span>Delivery Address / Street</span>
            <input
              required
              placeholder="House/Flat number, Street name, Landmark"
              value={form.address}
              onChange={(e) => setForm({ ...form, address: e.target.value })}
            />
          </label>
          <div className="two">
            <label className="field">
              <span>City</span>
              <input
                required
                placeholder="e.g. Bengaluru"
                value={form.city}
                onChange={(e) => setForm({ ...form, city: e.target.value })}
              />
            </label>
            <label className="field">
              <span>State</span>
              <input
                required
                placeholder="e.g. Karnataka"
                value={form.state}
                onChange={(e) => setForm({ ...form, state: e.target.value })}
              />
            </label>
          </div>
          <label className="field">
            <span>Pincode / Postal Code</span>
            <input
              required
              placeholder="e.g. 560001"
              value={form.pincode}
              onChange={(e) => setForm({ ...form, pincode: e.target.value })}
            />
          </label>
          <button
            type="submit"
            className="button wide"
            disabled={submitting}
            style={{ opacity: submitting ? 0.7 : 1 }}
          >
            {submitting ? 'Placing Order...' : 'Place Order'} <Check size={17} />
          </button>
        </form>

        <aside className="summary">
          <span className="eyebrow">Order summary</span>
          {cart.map((item) => (
            <div key={item.id}>
              <span>
                {item.product_name} × {item.quantity} {item.unit}
              </span>
              <b>₹{(item.price * item.quantity).toFixed(2)}</b>
            </div>
          ))}
          <hr style={{ border: '0', borderTop: '1px solid #cedacb', margin: '14px 0' }} />
          <strong>
            Total <b>₹{total.toFixed(2)}</b>
          </strong>
        </aside>
      </div>
    </main>
  );
}
