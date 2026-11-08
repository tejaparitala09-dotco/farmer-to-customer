import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, Minus, Plus, ShoppingBasket, X } from 'lucide-react';

export default function Cart({ cart, update, remove }) {
  const navigate = useNavigate();
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <main className="page section narrow">
      <div className="page-intro">
        <span className="eyebrow">Your harvest basket</span>
        <h1>Ready when <em>you are.</em></h1>
        <p>Review the freshly harvested produce in your cart before checking out.</p>
      </div>

      {cart.length === 0 ? (
        <div className="empty">
          <ShoppingBasket size={52} style={{ color: '#9bb195', marginBottom: 16 }} />
          <h2>Your basket is empty.</h2>
          <p>Add fresh vegetables, fruits, or staple groceries from our farmers.</p>
          <Link className="button" to="/products" style={{ marginTop: 15 }}>
            Browse produce <ArrowRight size={16} />
          </Link>
        </div>
      ) : (
        <>
          <div className="cart-list">
            {cart.map((item) => (
              <div className="cart-item" key={item.id}>
                <img
                  src={item.image_url || 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300'}
                  alt={item.product_name}
                  onError={(e) => {
                    e.currentTarget.src = 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300';
                  }}
                />
                <div>
                  <h3>{item.product_name}</h3>
                  <p>₹{item.price} / {item.unit}</p>
                </div>
                <div className="quantity">
                  <button
                    type="button"
                    onClick={() => update(item.id, item.quantity - 1)}
                    aria-label="Decrease quantity"
                  >
                    <Minus size={14} />
                  </button>
                  <b>{item.quantity}</b>
                  <button
                    type="button"
                    onClick={() => update(item.id, item.quantity + 1)}
                    disabled={item.quantity >= item.quantity_available}
                    aria-label="Increase quantity"
                  >
                    <Plus size={14} />
                  </button>
                </div>
                <strong>₹{(item.price * item.quantity).toFixed(2)}</strong>
                <button
                  className="icon-button"
                  type="button"
                  onClick={() => remove(item.id)}
                  title="Remove item"
                  aria-label={`Remove ${item.product_name}`}
                >
                  <X size={17} />
                </button>
              </div>
            ))}
          </div>

          <div className="cart-total">
            <span>Total amount</span>
            <strong>₹{total.toFixed(2)}</strong>
            <button className="button" onClick={() => navigate('/checkout')}>
              Proceed to checkout <ArrowRight size={17} />
            </button>
          </div>
        </>
      )}
    </main>
  );
}
