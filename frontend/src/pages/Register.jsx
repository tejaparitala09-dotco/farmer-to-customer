import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import * as api from '../api';

export default function Register({ setUser }) {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    phone: '',
    role: 'customer',
  });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    setError('');

    if (!form.name.trim() || form.name.length < 2) {
      setError('Please provide your full name (at least 2 characters).');
      return;
    }
    if (!form.email.trim()) {
      setError('Please provide a valid email address.');
      return;
    }
    if (!form.password || form.password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    setBusy(true);
    try {
      const res = await api.register({
        name: form.name.trim(),
        email: form.email.trim(),
        password: form.password,
        phone: form.phone.trim(),
        role: form.role,
      });

      localStorage.setItem('ftc_token', res.token);
      setUser(res.user);

      if (res.user.role === 'farmer') {
        navigate('/dashboard');
      } else {
        navigate('/products');
      }
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="narrow page auth-page">
      <div className="auth-art">
        <span className="eyebrow light">Join the table</span>
        <h1>
          Grow with us.<br />
          <em>Eat better.</em>
        </h1>
        <p style={{ marginTop: 20, color: '#cedacb', fontSize: 14 }}>
          Whether you cultivate the land or cherish wholesome home-cooked meals, welcome to our community.
        </p>
      </div>

      <form className="form-card" onSubmit={handleSubmit}>
        <span className="eyebrow">Start here</span>
        <h1>Join the table.</h1>

        {error && <div className="notice error">{error}</div>}

        <label className="field">
          <span>Full Name or Farm Name</span>
          <input
            required
            placeholder="e.g. Ramesh Kumar or Green Valley Farm"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
        </label>

        <label className="field">
          <span>Email Address</span>
          <input
            required
            type="email"
            placeholder="you@domain.com"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
        </label>

        <label className="field">
          <span>Phone Number</span>
          <input
            type="tel"
            placeholder="e.g. +91 9876543210"
            value={form.phone}
            onChange={(e) => setForm({ ...form, phone: e.target.value })}
          />
        </label>

        <label className="field">
          <span>Password (min. 6 characters)</span>
          <input
            required
            type="password"
            placeholder="Create a strong password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
        </label>

        <label className="field">
          <span>I am joining as</span>
          <select
            value={form.role}
            onChange={(e) => setForm({ ...form, role: e.target.value })}
          >
            <option value="customer">Customer (I want to buy fresh food)</option>
            <option value="farmer">Farmer (I want to sell my harvest)</option>
          </select>
        </label>

        <button
          type="submit"
          className="button wide"
          disabled={busy}
          style={{ opacity: busy ? 0.7 : 1 }}
        >
          {busy ? 'Creating Account...' : 'Create Account'} <ArrowRight size={17} />
        </button>

        <p className="switch">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </form>
    </main>
  );
}
