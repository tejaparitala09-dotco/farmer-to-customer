import { Link } from 'react-router-dom';
import { ShoppingBasket } from 'lucide-react';

export default function ProductCard({ product, add }) {
  const isOutOfStock = product.quantity <= 0;

  return (
    <article className="product-card">
      <Link to={`/products/${product.id}`}>
        <img
          src={product.image_url || 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600'}
          alt={product.product_name}
          loading="lazy"
          onError={(e) => {
            e.currentTarget.src = 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600';
          }}
        />
      </Link>
      <div className="product-info">
        <span className="eyebrow">{product.category}</span>
        <Link to={`/products/${product.id}`}>
          <h3>{product.product_name}</h3>
        </Link>
        <p className="muted">
          {isOutOfStock ? (
            <span style={{ color: '#a04432', fontWeight: 600 }}>Out of Stock</span>
          ) : (
            `${product.quantity} ${product.unit} available`
          )}
        </p>
        <div className="product-row">
          <strong>
            ₹{product.price}
            <small> / {product.unit}</small>
          </strong>
          <button
            className="button small"
            onClick={() => add(product)}
            disabled={isOutOfStock}
            title={isOutOfStock ? 'Currently out of stock' : 'Add to cart'}
          >
            Add <ShoppingBasket size={14} />
          </button>
        </div>
      </div>
    </article>
  );
}
