import { useState } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import * as api from '../api';

export default function Login({ setUser }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    setError('');

    if (!form.email.trim() || !form.password) {
      setError('Please enter both your email and password.');
      return;
    }

    setBusy(true);
    try {
      const res = await api.login({
        email: form.email.trim(),
        password: form.password,
      });

      localStorage.setItem('ftc_token', res.token);
      setUser(res.user);

      const redirectPath =
        location.state?.from?.pathname ||
        (res.user.role === 'farmer' ? '/dashboard' : '/products');
      navigate(redirectPath, { replace: true });
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="narrow page auth-page">
      <div className="auth-art">
        <span className="eyebrow light">Direct Farm to Table</span>
        <h1>
          Food feels<br />
          <em>better</em> closer.
        </h1>
        <p style={{ marginTop: 20, color: '#cedacb', fontSize: 14 }}>
          Connect with trusted local agriculturalists and relish honest, seasonal food.
        </p>
      </div>

      <form className="form-card" onSubmit={handleSubmit}>
        <span className="eyebrow">Welcome back</span>
        <h1>Sign in.</h1>

        {error && <div className="notice error">{error}</div>}

        <label className="field">
          <span>Email Address</span>
          <input
            required
            type="email"
            placeholder="farmer@farm.com or you@domain.com"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
        </label>

        <label className="field">
          <span>Password</span>
          <input
            required
            type="password"
            placeholder="Your account password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
        </label>

        <button
          type="submit"
          className="button wide"
          disabled={busy}
          style={{ opacity: busy ? 0.7 : 1 }}
        >
          {busy ? 'Signing In...' : 'Sign In'} <ArrowRight size={17} />
        </button>

        <p className="switch">
          New here? <Link to="/register">Create an account</Link>
        </p>
      </form>
    </main>
  );
}
