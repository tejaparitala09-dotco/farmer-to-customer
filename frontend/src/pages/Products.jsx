import { useEffect, useState } from 'react';
import { Search, ShoppingBasket } from 'lucide-react';
import ProductCard from '../components/ProductCard';
import Loading from '../components/Loading';
import * as api from '../api';

const categories = [
  'All',
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

export default function Products({ add }) {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [sort, setSort] = useState('name');
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setBusy(true);
    setError('');
    api.getProducts(search, category === 'All' ? '' : category)
      .then((data) => {
        setProducts(data);
      })
      .catch((err) => {
        setError(err.message || 'Failed to load products');
        setProducts([]);
      })
      .finally(() => setBusy(false));
  }, [search, category]);

  const sortedProducts = [...products].sort((a, b) => {
    if (sort === 'price-asc') return a.price - b.price;
    if (sort === 'price-desc') return b.price - a.price;
    return a.product_name.localeCompare(b.product_name);
  });

  return (
    <main className="page section">
      <div className="page-intro">
        <span className="eyebrow">The seasonal harvest</span>
        <h1>Fresh produce, <em>honestly sourced.</em></h1>
        <p>Browse fresh farm-grown vegetables, orchard fruits, whole grains, and rural grocery staples.</p>
      </div>

      <div className="toolbar">
        <label className="search">
          <Search size={18} />
          <input
            placeholder="Search tomatoes, mangoes, basmati rice..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </label>
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c === 'All' ? 'All Categories' : c}
            </option>
          ))}
        </select>
        <select value={sort} onChange={(e) => setSort(e.target.value)}>
          <option value="name">Sort: Name (A-Z)</option>
          <option value="price-asc">Sort: Price (Low to High)</option>
          <option value="price-desc">Sort: Price (High to Low)</option>
        </select>
      </div>

      {error && <div className="notice error">{error}</div>}

      {busy ? (
        <Loading />
      ) : sortedProducts.length === 0 ? (
        <div className="empty">
          <ShoppingBasket size={44} style={{ color: '#9bb195', marginBottom: 12 }} />
          <h2>No products found</h2>
          <p>Try refining your search keyword or selecting a different category.</p>
        </div>
      ) : (
        <div className="product-grid">
          {sortedProducts.map((p) => (
            <ProductCard key={p.id} product={p} add={add} />
          ))}
        </div>
      )}
    </main>
  );
}
