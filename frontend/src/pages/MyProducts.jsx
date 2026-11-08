import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Trash2 } from 'lucide-react';
import Loading from '../components/Loading';
import * as api from '../api';

export default function MyProducts() {
  const [items, setItems] = useState([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const loadItems = () => {
    setBusy(true);
    setError('');
    api.myProducts()
      .then((data) => setItems(data))
      .catch((err) => setError(err.message || 'Failed to load your products'))
      .finally(() => setBusy(false));
  };

  useEffect(() => {
    loadItems();
  }, []);

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to remove "${name}" from your catalog?`)) {
      return;
    }
    try {
      await api.deleteProduct(id);
      setItems((prev) => prev.filter((p) => p.id !== id));
      setNotice(`"${name}" was removed successfully.`);
      setTimeout(() => setNotice(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to delete product');
    }
  };

  return (
    <main className="page section">
      <div className="section-heading">
        <div>
          <span className="eyebrow">Your farm harvest</span>
          <h1>My products.</h1>
        </div>
        <Link className="button" to="/add-product">
          Add product <Plus size={17} />
        </Link>
      </div>

      {notice && <div className="notice">{notice}</div>}
      {error && <div className="notice error">{error}</div>}

      {busy ? (
        <Loading />
      ) : items.length === 0 ? (
        <div className="empty">
          <h2>No products listed yet.</h2>
          <p>Start selling your fresh harvest directly to local families.</p>
          <Link className="button" to="/add-product" style={{ marginTop: 15 }}>
            Publish your first produce <Plus size={17} />
          </Link>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>Category</th>
                <th>Price</th>
                <th>Available Stock</th>
                <th style={{ textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td>
                    <img
                      className="table-img"
                      src={item.image_url || 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100'}
                      alt=""
                      onError={(e) => {
                        e.currentTarget.src = 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100';
                      }}
                    />
                    <strong>{item.product_name}</strong>
                  </td>
                  <td>{item.category}</td>
                  <td>
                    ₹{item.price} / {item.unit}
                  </td>
                  <td>
                    {item.quantity} {item.unit}
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <button
                      className="link-button danger"
                      onClick={() => handleDelete(item.id, item.product_name)}
                      title="Delete Product"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}
