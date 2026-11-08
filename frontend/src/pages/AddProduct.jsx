import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import * as api from '../api';

const categories = [
  'Vegetables',
  'Fruits',
  'Grains',
  'Millets',
  'Pulses',
  'Spices',
  'Dairy',
  'Grocery',
  'Other',
];

const units = ['kg', 'dozen', 'bunch', 'piece', 'litre', 'bottle', 'packet'];

export default function AddProduct() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    product_name: '',
    category: 'Vegetables',
    price: '',
    unit: 'kg',
    quantity: '',
    description: '',
    image_url: '',
  });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const update = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    setError('');

    if (!form.product_name.trim() || form.product_name.length < 2) {
      setError('Please provide a valid product name (at least 2 letters).');
      return;
    }
    const numPrice = Number(form.price);
    if (isNaN(numPrice) || numPrice <= 0) {
      setError('Price must be greater than 0.');
      return;
    }
    const numQty = Number(form.quantity);
    if (isNaN(numQty) || numQty < 0) {
      setError('Quantity cannot be negative.');
      return;
    }
    if (!form.description.trim() || form.description.length < 2) {
      setError('Please describe your product for customers.');
      return;
    }

    setBusy(true);
    try {
      await api.addProduct({
        product_name: form.product_name.trim(),
        category: form.category,
        price: numPrice,
        unit: form.unit,
        quantity: numQty,
        description: form.description.trim(),
        image_url: form.image_url.trim(),
      });
      navigate('/my-products');
    } catch (err) {
      setError(err.message || 'Failed to publish product');
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="page narrow section">
      <Link className="back" to="/my-products">
        ← Back to my products
      </Link>
      <form className="form-card" onSubmit={handleSubmit}>
        <span className="eyebrow">Add to the harvest</span>
        <h1>New product.</h1>

        {error && <div className="notice error">{error}</div>}

        <label className="field">
          <span>Product Name</span>
          <input
            required
            name="product_name"
            placeholder="e.g. Organic Roma Tomatoes"
            value={form.product_name}
            onChange={update}
          />
        </label>

        <div className="two">
          <label className="field">
            <span>Price (₹)</span>
            <input
              required
              name="price"
              type="number"
              step="any"
              min="0.5"
              placeholder="e.g. 40"
              value={form.price}
              onChange={update}
            />
          </label>
          <label className="field">
            <span>Unit of Measurement</span>
            <select name="unit" value={form.unit} onChange={update}>
              {units.map((u) => (
                <option key={u} value={u}>
                  {u}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="two">
          <label className="field">
            <span>Category</span>
            <select name="category" value={form.category} onChange={update}>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </label>
          <label className="field">
            <span>Available Stock</span>
            <input
              required
              name="quantity"
              type="number"
              step="any"
              min="0"
              placeholder="e.g. 100"
              value={form.quantity}
              onChange={update}
            />
          </label>
        </div>

        <label className="field">
          <span>Description</span>
          <input
            required
            name="description"
            placeholder="Fresh, harvested this morning without synthetic pesticides."
            value={form.description}
            onChange={update}
          />
        </label>

        <label className="field">
          <span>Image URL (optional)</span>
          <input
            name="image_url"
            placeholder="https://images.unsplash.com/..."
            value={form.image_url}
            onChange={update}
          />
        </label>

        <button
          type="submit"
          className="button wide"
          disabled={busy}
          style={{ opacity: busy ? 0.7 : 1 }}
        >
          {busy ? 'Publishing...' : 'Publish Product'} <ArrowRight size={17} />
        </button>
      </form>
    </main>
  );
}
