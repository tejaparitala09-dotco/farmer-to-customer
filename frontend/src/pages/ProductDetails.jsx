import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Minus, Plus, ShoppingBasket } from 'lucide-react';
import Loading from '../components/Loading';
import * as api from '../api';

export default function ProductDetails({ add }) {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [qty, setQty] = useState(1);
  const [error, setError] = useState('');
  const [addedNotice, setAddedNotice] = useState(false);

  useEffect(() => {
    if (!id) return;
    setError('');
    api.getProduct(id)
      .then((data) => {
        setProduct(data);
      })
      .catch((err) => {
        setError(err.message || 'Product could not be loaded');
      });
  }, [id]);

  if (error) {
    return (
      <main className="page section narrow">
        <Link className="back" to="/products">← Back to produce</Link>
        <div className="notice error">{error}</div>
      </main>
    );
  }

  if (!product) return <Loading />;

  const isOutOfStock = product.quantity <= 0;
  const maxAvailable = Math.max(1, product.quantity);

  const handleAddToCart = () => {
    if (isOutOfStock) return;
    add(product, qty);
    setAddedNotice(true);
    setTimeout(() => setAddedNotice(false), 2500);
  };

  return (
    <main className="page section">
      <Link className="back" to="/products">← Back to produce</Link>
      {addedNotice && (
        <div className="notice" style={{ maxWidth: 600, marginBottom: 20 }}>
          Added {qty} {product.unit} of {product.product_name} to your basket!
        </div>
      )}
      <div className="detail">
        <img
          src={product.image_url || 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=900'}
          alt={product.product_name}
          onError={(e) => {
            e.currentTarget.src = 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=900';
          }}
        />
        <div className="detail-copy">
          <span className="eyebrow">{product.category}</span>
          <h1>{product.product_name}</h1>
          <p className="price">
            ₹{product.price}
            <small> / {product.unit}</small>
          </p>
          <p>{product.description}</p>
          <p className="stock">
            {isOutOfStock ? (
              <span style={{ color: '#a04432', fontWeight: 600 }}>Currently Out of Stock</span>
            ) : (
              `${product.quantity} ${product.unit} available · Fresh from ${product.farmer_name || 'Local Farm'}`
            )}
          </p>

          {!isOutOfStock && (
            <div className="quantity">
              <button
                type="button"
                onClick={() => setQty(Math.max(1, qty - 1))}
                aria-label="Decrease quantity"
              >
                <Minus size={16} />
              </button>
              <b>{qty}</b>
              <button
                type="button"
                onClick={() => setQty(Math.min(maxAvailable, qty + 1))}
                aria-label="Increase quantity"
              >
                <Plus size={16} />
              </button>
            </div>
          )}

          <button
            className="button"
            onClick={handleAddToCart}
            disabled={isOutOfStock}
            style={{ opacity: isOutOfStock ? 0.6 : 1 }}
          >
            {isOutOfStock ? 'Out of Stock' : `Add ${qty} to cart`} <ShoppingBasket size={17} />
          </button>
        </div>
      </div>
    </main>
  );
}
