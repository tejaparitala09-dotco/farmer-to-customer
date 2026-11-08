import React from 'react';
import { ArrowRight, Check, Edit3, Leaf, Minus, Plus, Search, ShoppingCart, Trash2, X } from 'lucide-react';
import { getApiErrorMessage, orderApi, productApi } from './api';

const categories = ['All', 'Vegetables', 'Fruits', 'Grains', 'Dairy', 'Other'];
const orderStatuses = ['Pending', 'Confirmed', 'Shipped', 'Out for Delivery', 'Delivered', 'Cancelled'];
const trackingStatuses = ['Pending', 'Confirmed', 'Shipped', 'Out for Delivery', 'Delivered'];
const emptyProduct = { product_name: '', category: 'Vegetables', price: '', unit: 'kg', quantity: '', description: '', image_url: '' };

function LoadingMessage({ children = 'Loading fresh products...' }) {
  return <p className="market-message">{children}</p>;
}

function ProductCard({ product, onSelect, onAdd }) {
  return (
    <article className="product-card">
      <button className="product-image-wrap product-image-button" type="button" onClick={() => onSelect(product)}>
        {product.image_url ? <img src={product.image_url} alt={product.product_name} loading="lazy" /> : <div className="image-fallback"><Leaf size={36} /></div>}
        <span className="product-category">{product.category}</span>
      </button>
      <div className="product-info">
        <div className="product-title-row"><h3>{product.product_name}</h3><span>${product.price.toFixed(2)} / {product.unit}</span></div>
        <p className="farmer-name"><Leaf size={13} /> {product.farmer_name}</p>
        <button className="add-button" type="button" onClick={() => onAdd(product)}><span>Add to Cart</span><ShoppingCart size={15} /></button>
      </div>
    </article>
  );
}

function ProductDetail({ product, onClose, onAdd }) {
  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div className="product-detail-modal" role="dialog" aria-modal="true" aria-label={product.product_name} onClick={(event) => event.stopPropagation()}>
        <button className="modal-close" type="button" aria-label="Close product details" onClick={onClose}><X size={19} /></button>
        {product.image_url ? <img src={product.image_url} alt={product.product_name} /> : <div className="detail-fallback"><Leaf size={52} /></div>}
        <div className="product-detail-copy"><p className="eyebrow"><span /> {product.category}</p><h2>{product.product_name}</h2><p className="detail-farmer">Grown by {product.farmer_name}</p><p>{product.description || 'Freshly grown and shared directly from a local farm.'}</p><strong>${product.price.toFixed(2)} / {product.unit}</strong><button className="auth-submit" type="button" onClick={() => { onAdd(product); onClose(); }}>Add to Cart <ShoppingCart size={17} /></button></div>
      </div>
    </div>
  );
}

function CartPanel({ cart, onClose, onUpdateQuantity, onRemove, onCheckout, checkoutLoading }) {
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  return (
    <div className="cart-panel">
      <div className="cart-heading"><div><p className="eyebrow"><span /> Your basket</p><h2>Cart <em>({cart.length})</em></h2></div><button className="modal-close" type="button" aria-label="Close cart" onClick={onClose}><X size={19} /></button></div>
      {cart.length === 0 ? <p className="market-message">Your basket is waiting for something good.</p> : <>
        <div className="cart-items">{cart.map((item) => <div className="cart-item" key={item.id}><div><strong>{item.product_name}</strong><small>${item.price.toFixed(2)} / {item.unit}</small></div><div className="quantity-control"><button type="button" aria-label={`Decrease ${item.product_name}`} onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}><Minus size={13} /></button><span>{item.quantity}</span><button type="button" aria-label={`Increase ${item.product_name}`} onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}><Plus size={13} /></button><button className="remove-item" type="button" aria-label={`Remove ${item.product_name}`} onClick={() => onRemove(item.id)}><Trash2 size={14} /></button></div></div>)}</div>
        <div className="cart-total"><span>Total</span><strong>${total.toFixed(2)}</strong></div>
        <button className="auth-submit" type="button" onClick={onCheckout} disabled={checkoutLoading}>{checkoutLoading ? 'Placing order...' : 'Place Order'} <ArrowRight size={17} /></button>
      </>}
    </div>
  );
}

function OrderTracking({ status }) {
  const currentIndex = trackingStatuses.indexOf(status);
  return <div className="order-tracking" aria-label={`Order status: ${status}`}>{trackingStatuses.map((step, index) => <React.Fragment key={step}><div className={index <= currentIndex ? 'tracking-step complete' : 'tracking-step'}><span>{index < currentIndex ? '✓' : index + 1}</span><small>{step}</small></div>{index < trackingStatuses.length - 1 && <div className={index < currentIndex ? 'tracking-line complete' : 'tracking-line'} />}</React.Fragment>)}</div>;
}

export function MarketplaceSection({ currentUser, navigate }) {
  const [products, setProducts] = React.useState([]);
  const [category, setCategory] = React.useState('All');
  const [search, setSearch] = React.useState('');
  const [cart, setCart] = React.useState([]);
  const [detail, setDetail] = React.useState(null);
  const [cartOpen, setCartOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(true);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [checkoutLoading, setCheckoutLoading] = React.useState(false);

  async function loadProducts() {
    setLoading(true);
    setErrorMessage('');
    try {
      const response = await productApi.list({ ...(search ? { search } : {}), ...(category !== 'All' ? { category } : {}) });
      setProducts(response.data);
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error));
    } finally {
      setLoading(false);
    }
  }

  React.useEffect(() => {
    const timer = window.setTimeout(loadProducts, 250);
    return () => window.clearTimeout(timer);
  }, [search, category]);

  function addToCart(product) {
    setCart((items) => {
      const existing = items.find((item) => item.id === product.id);
      if (existing) return items.map((item) => item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item);
      return [...items, { ...product, quantity: 1 }];
    });
    setCartOpen(true);
  }

  function updateQuantity(productId, quantity) {
    if (quantity <= 0) return setCart((items) => items.filter((item) => item.id !== productId));
    setCart((items) => items.map((item) => item.id === productId ? { ...item, quantity: Math.min(quantity, item.quantity) } : item));
  }

  async function checkout() {
    if (!currentUser) return navigate('login');
    if (currentUser.role !== 'customer') return navigate('customer');
    const address = window.prompt('Enter your delivery address');
    if (!address?.trim()) return;
    setCheckoutLoading(true);
    try {
      await orderApi.create({ items: cart.map((item) => ({ product_id: item.id, quantity: item.quantity })), delivery_address: address.trim() });
      setCart([]);
      setCartOpen(false);
      navigate('customer?order=success');
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error));
    } finally {
      setCheckoutLoading(false);
    }
  }

  const cartCount = cart.reduce((total, item) => total + item.quantity, 0);
  return (
    <section className="marketplace" id="products">
      <div className="section-heading"><div><p className="eyebrow"><span /> From our farmers</p><h2>Shop the <em>harvest.</em></h2></div><p className="section-description">Everything you need, grown with intention and delivered from a farm you can know.</p></div>
      <div className="marketplace-toolbar"><div className="search-box"><Search size={16} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search products" aria-label="Search products" /></div><button className="cart-toggle" type="button" onClick={() => setCartOpen(true)}><ShoppingCart size={16} /> Cart <span>{cartCount}</span></button></div>
      <div className="category-row marketplace-categories">{categories.map((item) => <button className={category === item ? 'category-card selected' : 'category-card'} type="button" key={item} onClick={() => setCategory(item)}><span className="category-icon"><Leaf size={22} /></span><span><strong>{item}</strong><small>{item === 'All' ? 'All products' : 'Browse fresh'}</small></span></button>)}</div>
      {errorMessage && <p className="form-error" role="alert">{errorMessage}</p>}
      <div className="catalog-heading"><p>{category === 'All' ? 'Fresh from the database' : category}</p><span>{products.length} products available</span></div>
      {loading ? <LoadingMessage /> : products.length === 0 ? <p className="market-message">No products match your search yet.</p> : <div className="product-grid">{products.map((product) => <ProductCard key={product.id} product={product} onSelect={setDetail} onAdd={addToCart} />)}</div>}
      {detail && <ProductDetail product={detail} onClose={() => setDetail(null)} onAdd={addToCart} />}
      {cartOpen && <CartPanel cart={cart} onClose={() => setCartOpen(false)} onUpdateQuantity={updateQuantity} onRemove={(id) => setCart((items) => items.filter((item) => item.id !== id))} onCheckout={checkout} checkoutLoading={checkoutLoading} />}
    </section>
  );
}

function ProductForm({ initialProduct, onSave, onCancel, saving }) {
  const [form, setForm] = React.useState(initialProduct || emptyProduct);
  function update(field, value) { setForm((current) => ({ ...current, [field]: value })); }
  function submit(event) { event.preventDefault(); onSave({ ...form, price: Number(form.price), quantity: Number(form.quantity) }); }
  return <form className="dashboard-form" onSubmit={submit}><div className="form-grid"><label><span>Product name</span><input value={form.product_name} onChange={(event) => update('product_name', event.target.value)} required /></label><label><span>Category</span><select value={form.category} onChange={(event) => update('category', event.target.value)}>{categories.slice(1).map((item) => <option key={item}>{item}</option>)}</select></label><label><span>Price</span><input type="number" min="0.01" step="0.01" value={form.price} onChange={(event) => update('price', event.target.value)} required /></label><label><span>Unit</span><input value={form.unit} onChange={(event) => update('unit', event.target.value)} placeholder="kg, bunch, litre" required /></label><label><span>Quantity available</span><input type="number" min="0.01" step="0.01" value={form.quantity} onChange={(event) => update('quantity', event.target.value)} required /></label><label><span>Image URL</span><input type="url" value={form.image_url} onChange={(event) => update('image_url', event.target.value)} placeholder="https://..." /></label></div><label><span>Description</span><textarea rows="4" value={form.description} onChange={(event) => update('description', event.target.value)} /></label><div className="form-actions"><button className="auth-submit" type="submit" disabled={saving}>{saving ? 'Saving...' : initialProduct ? 'Save changes' : 'Add product'} <Check size={17} /></button>{initialProduct && <button className="button button-secondary" type="button" onClick={onCancel}>Cancel</button>}</div></form>;
}

function OrdersList({ orders, farmer, onStatusChange, updatingOrder }) {
  if (!orders.length) return <p className="market-message">No orders yet.</p>;
  return <div className="orders-list">{orders.map((order) => <article className="order-card" key={order.id}><div className="order-card-heading"><div><strong>Order {order.id.slice(0, 8)}</strong><small>{new Date(order.created_at).toLocaleDateString()}</small></div>{farmer ? <select value={order.status} disabled={updatingOrder === order.id} onChange={(event) => onStatusChange(order.id, event.target.value)}>{orderStatuses.map((status) => <option key={status}>{status}</option>)}</select> : <span className="order-status">{order.status}</span>}</div><OrderTracking status={order.status} /><div className="order-items">{order.items.map((item) => <span key={`${order.id}-${item.product_id}`}>{item.product_name} x {item.quantity}</span>)}</div><div className="order-card-footer"><span>{farmer ? `Customer: ${order.customer_name}` : `Deliver to: ${order.delivery_address}`}</span><strong>${order.total_amount.toFixed(2)}</strong></div></article>)}</div>;
}

export function CustomerDashboard({ user, navigate, orderSuccess = false }) {
  const [orders, setOrders] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [errorMessage, setErrorMessage] = React.useState('');
  React.useEffect(() => { orderApi.mine().then((response) => setOrders(response.data)).catch((error) => setErrorMessage(getApiErrorMessage(error))).finally(() => setLoading(false)); }, []);
  return <main className="dashboard-page"><div className="dashboard-heading"><div><p className="eyebrow"><span /> Customer account</p><h1>Your <em>orders.</em></h1><p>Welcome back, {user.full_name}. Keep track of every farm-fresh delivery.</p></div><button className="button button-primary" type="button" onClick={() => navigate('home')}>Shop products <ArrowRight size={17} /></button></div>{orderSuccess && <p className="form-success order-success" role="status">Order placed successfully. You can track its delivery status below.</p>}<section className="dashboard-section"><div className="dashboard-section-heading"><h2>Order history</h2><span>{orders.length} orders</span></div>{errorMessage && <p className="form-error" role="alert">{errorMessage}</p>}{loading ? <LoadingMessage>Loading your orders...</LoadingMessage> : <OrdersList orders={orders} />}</section></main>;
}

export function FarmerDashboard({ user, navigate, addProductOnly = false }) {
  const [products, setProducts] = React.useState([]);
  const [orders, setOrders] = React.useState([]);
  const [editing, setEditing] = React.useState(null);
  const [showForm, setShowForm] = React.useState(addProductOnly);
  const [loading, setLoading] = React.useState(true);
  const [saving, setSaving] = React.useState(false);
  const [updatingOrder, setUpdatingOrder] = React.useState(null);
  const [errorMessage, setErrorMessage] = React.useState('');
  async function load() { setLoading(true); try { const [productResponse, orderResponse] = await Promise.all([productApi.mine(), orderApi.farmerOrders()]); setProducts(productResponse.data); setOrders(orderResponse.data); } catch (error) { setErrorMessage(getApiErrorMessage(error)); } finally { setLoading(false); } }
  React.useEffect(() => { load(); }, []);
  React.useEffect(() => { setShowForm(addProductOnly); if (addProductOnly) setEditing(null); }, [addProductOnly]);
  async function saveProduct(payload) { setSaving(true); setErrorMessage(''); try { if (editing) await productApi.update(editing.id, payload); else await productApi.create(payload); setEditing(null); setShowForm(false); await load(); if (addProductOnly) navigate('farmer'); } catch (error) { setErrorMessage(getApiErrorMessage(error)); } finally { setSaving(false); } }
  async function deleteProduct(id) { if (!window.confirm('Delete this product?')) return; try { await productApi.remove(id); await load(); } catch (error) { setErrorMessage(getApiErrorMessage(error)); } }
  async function updateStatus(orderId, nextStatus) { setUpdatingOrder(orderId); try { await orderApi.updateStatus(orderId, nextStatus); await load(); } catch (error) { setErrorMessage(getApiErrorMessage(error)); } finally { setUpdatingOrder(null); } }
  const pendingOrders = orders.filter((order) => order.status === 'Pending').length;
  const deliveredOrders = orders.filter((order) => order.status === 'Delivered').length;
  const totalSales = orders.reduce((total, order) => total + order.total_amount, 0);
  return <main className="dashboard-page"><div className="dashboard-heading"><div><p className="eyebrow"><span /> Farmer space</p><h1>Grow your <em>market.</em></h1><p>Welcome back, {user.full_name}. Manage your harvest and customer orders.</p></div><button className="button button-primary" type="button" onClick={() => navigate('farmer-add-product')}>Add product <Plus size={17} /></button></div>{errorMessage && <p className="form-error" role="alert">{errorMessage}</p>}<section className="stat-grid"><article className="stat-card"><span>Total Products</span><strong>{products.length}</strong></article><article className="stat-card"><span>Total Orders</span><strong>{orders.length}</strong></article><article className="stat-card"><span>Pending Orders</span><strong>{pendingOrders}</strong></article><article className="stat-card"><span>Delivered Orders</span><strong>{deliveredOrders}</strong></article><article className="stat-card stat-card-accent"><span>Total Sales</span><strong>${totalSales.toFixed(2)}</strong></article></section>{showForm && <section className="dashboard-section"><div className="dashboard-section-heading"><h2>{editing ? 'Edit product' : 'New product'}</h2><button className="modal-close" type="button" onClick={() => addProductOnly ? navigate('farmer') : setShowForm(false)}><X size={18} /></button></div><ProductForm initialProduct={editing} onSave={saveProduct} onCancel={() => { setEditing(null); setShowForm(false); }} saving={saving} /></section>}{!addProductOnly && <><section className="dashboard-section"><div className="dashboard-section-heading"><h2>Your products</h2><span>{products.length} products</span></div>{loading ? <LoadingMessage>Loading your products...</LoadingMessage> : products.length === 0 ? <p className="market-message">Add your first product to start selling.</p> : <div className="farmer-product-list">{products.map((product) => <article className="farmer-product-row" key={product.id}><div><strong>{product.product_name}</strong><small>{product.category} · ${product.price.toFixed(2)} / {product.unit} · {product.quantity} available</small></div><div><button className="icon-action" type="button" aria-label={`Edit ${product.product_name}`} onClick={() => { setEditing(product); setShowForm(true); }}><Edit3 size={16} /></button><button className="icon-action danger" type="button" aria-label={`Delete ${product.product_name}`} onClick={() => deleteProduct(product.id)}><Trash2 size={16} /></button></div></article>)}</div>}</section><section className="dashboard-section"><div className="dashboard-section-heading"><h2>Customer orders</h2><span>{orders.length} orders</span></div>{loading ? <LoadingMessage>Loading orders...</LoadingMessage> : <OrdersList orders={orders} farmer onStatusChange={updateStatus} updatingOrder={updatingOrder} />}</section></>}</main>;
}
