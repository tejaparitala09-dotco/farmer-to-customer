import React from 'react';
import { createRoot } from 'react-dom/client';
import { Apple, ArrowRight, Carrot, Check, Clock3, Leaf, LockKeyhole, Mail, Menu, Milk, Phone, ShieldCheck, ShoppingCart, Truck, UserRound, Wheat, X } from 'lucide-react';
import { authApi, authStorage, getApiErrorMessage } from './api';
import { CustomerDashboard, FarmerDashboard, MarketplaceSection } from './marketplace';
import './styles.css';

const features = [
  {
    icon: Leaf,
    number: '01',
    title: 'Fresh Products',
    description: 'Seasonal produce picked with care and delivered while it is at its best.',
  },
  {
    icon: ShieldCheck,
    number: '02',
    title: 'Fair Prices',
    description: 'A better deal for you and a more rewarding return for the people who grow it.',
  },
  {
    icon: Truck,
    number: '03',
    title: 'Fast Delivery',
    description: 'Simple, dependable delivery from nearby farms straight to your doorstep.',
  },
];

const categories = [
  { icon: Carrot, name: 'Vegetables', detail: '24 products' },
  { icon: Apple, name: 'Fruits', detail: '18 products' },
  { icon: Wheat, name: 'Grains', detail: '12 products' },
  { icon: Milk, name: 'Dairy', detail: '9 products' },
];

const products = [
  {
    name: 'Garden Tomatoes',
    category: 'Vegetables',
    price: '$3.50 / kg',
    farmer: 'Maya Green Farm',
    image: 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=700&q=85',
  },
  {
    name: 'Sweet Carrots',
    category: 'Vegetables',
    price: '$2.80 / bunch',
    farmer: 'Riverbend Organics',
    image: 'https://images.unsplash.com/photo-1445282768818-728615cc910a?auto=format&fit=crop&w=700&q=85',
  },
  {
    name: 'Red Apples',
    category: 'Fruits',
    price: '$4.20 / kg',
    farmer: 'Sunny Orchard',
    image: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=700&q=85',
  },
  {
    name: 'Golden Corn',
    category: 'Grains',
    price: '$3.10 / 6 ears',
    farmer: 'Oakfield Farms',
    image: 'https://images.unsplash.com/photo-1601593768791-0e76f6d8b7b3?auto=format&fit=crop&w=700&q=85',
  },
  {
    name: 'Brown Rice',
    category: 'Grains',
    price: '$6.40 / kg',
    farmer: 'Harvest Lane Co-op',
    image: 'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?auto=format&fit=crop&w=700&q=85',
  },
  {
    name: 'Farm Fresh Milk',
    category: 'Dairy',
    price: '$5.25 / litre',
    farmer: 'Willow Creek Dairy',
    image: 'https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=700&q=85',
  },
];

function Brand() {
  return (
    <a className="brand" href="#home" aria-label="Farmer to Customer home">
      <span className="brand-mark"><Leaf size={18} strokeWidth={2.5} /></span>
      <span>farmer<span className="brand-accent">to</span>customer</span>
    </a>
  );
}

function Header({ menuOpen, setMenuOpen, currentUser, onLogout }) {
  return (
    <header className="site-header">
      <div className="header-inner">
        <Brand />
        <nav className={menuOpen ? 'main-nav is-open' : 'main-nav'} aria-label="Primary navigation">
          <a className="active" href="#home" onClick={() => setMenuOpen(false)}>Home</a>
          <a href="#products" onClick={() => setMenuOpen(false)}>Products</a>
          <a href="#about" onClick={() => setMenuOpen(false)}>About</a>
          <a href="#contact" onClick={() => setMenuOpen(false)}>Contact</a>
          {currentUser ? <>
            <a className="login-link" href={`#${currentUser.role}`} onClick={() => setMenuOpen(false)}>{currentUser.role === 'farmer' ? 'Farmer space' : 'My account'} <ArrowRight size={16} /></a>
            <button className="logout-link" type="button" onClick={onLogout}>Logout</button>
          </> : <a className="login-link" href="#login" onClick={() => setMenuOpen(false)}>Login <ArrowRight size={16} /></a>}
        </nav>
        <button className="menu-toggle" type="button" aria-label={menuOpen ? 'Close menu' : 'Open menu'} onClick={() => setMenuOpen(!menuOpen)}>
          {menuOpen ? <X size={23} /> : <Menu size={23} />}
        </button>
      </div>
    </header>
  );
}

function AuthPage({ mode, navigate, initialRole = 'Customer', onAuthenticated }) {
  const isLogin = mode === 'login';
  const [role, setRole] = React.useState(initialRole);
  const [submitted, setSubmitted] = React.useState(false);
  const [passwordsMatch, setPasswordsMatch] = React.useState(true);
  const [loading, setLoading] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState('');

  async function handleSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    setErrorMessage('');
    setSubmitted(false);

    if (!isLogin) {
      const passwordsAreEqual = formData.get('password') === formData.get('confirmPassword');
      setPasswordsMatch(passwordsAreEqual);
      if (!passwordsAreEqual) return;
    }

    setLoading(true);
    try {
      if (isLogin) {
        const response = await authApi.login({
          email: formData.get('email'),
          password: formData.get('password'),
        });
        authStorage.save(response.data.access_token, response.data.user);
        onAuthenticated(response.data.user);
        navigate(response.data.user.role);
      } else {
        await authApi.register(role.toLowerCase(), {
          full_name: formData.get('fullName'),
          email: formData.get('email'),
          phone_number: formData.get('phone'),
          password: formData.get('password'),
        });
        setSubmitted(true);
        form.reset();
        setRole('Customer');
      }
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <div className="auth-visual">
        <div className="auth-visual-copy">
          <p className="eyebrow"><span /> A closer food system</p>
          <h1>{isLogin ? <>Welcome <em>back.</em></> : <>Grow with<br /><em>us.</em></>}</h1>
          <p>{isLogin ? 'Pick up where you left off and discover what is fresh from nearby farms.' : 'Join a community making better food choices possible for everyone.'}</p>
        </div>
        <div className="auth-visual-note"><Leaf size={17} /> Fresh from people who care</div>
      </div>
      <div className="auth-panel">
        <button className="back-home" type="button" onClick={() => navigate('home')}><ArrowRight size={16} className="back-arrow" /> Back to home</button>
        <div className="auth-heading">
          <p className="eyebrow">{isLogin ? 'Your account' : 'Get started'}</p>
          <h2>{isLogin ? 'Log in to your account' : 'Create your account'}</h2>
          <p>{isLogin ? 'Welcome back. Please enter your details.' : 'A few details and you are ready to shop local.'}</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {!isLogin && <label><span>Full Name</span><div className="input-wrap"><UserRound size={17} /><input name="fullName" type="text" placeholder="Your full name" required /></div></label>}
          <label><span>Email</span><div className="input-wrap"><Mail size={17} /><input name="email" type="email" placeholder="you@example.com" required /></div></label>
          {!isLogin && <label><span>Phone Number</span><div className="input-wrap"><Phone size={17} /><input name="phone" type="tel" placeholder="Your phone number" required /></div></label>}
          <label><span>Password</span><div className="input-wrap"><LockKeyhole size={17} /><input name="password" type="password" placeholder={isLogin ? 'Enter your password' : 'Create a password'} required minLength="6" /></div></label>
          {!isLogin && <label><span>Confirm Password</span><div className="input-wrap"><LockKeyhole size={17} /><input name="confirmPassword" type="password" placeholder="Repeat your password" required minLength="6" /></div></label>}
          {!isLogin && <fieldset className="role-field"><legend>I am joining as a</legend><div className="role-options">
            {['Customer', 'Farmer'].map((option) => <label className={role === option ? 'role-option selected' : 'role-option'} key={option}><input type="radio" name="role" value={option} checked={role === option} onChange={() => setRole(option)} /><span>{option}</span>{role === option && <Check size={15} />}</label>)}
          </div></fieldset>}
          {!passwordsMatch && <p className="form-error">Passwords do not match. Please try again.</p>}
          {errorMessage && <p className="form-error" role="alert">{errorMessage}</p>}
          {submitted && <p className="form-success" role="status">Registration successful. You can now log in.</p>}
          <button className="auth-submit" type="submit" disabled={loading}>{loading ? 'Please wait...' : isLogin ? 'Login' : 'Register'} {!loading && <ArrowRight size={17} />}</button>
        </form>

        <p className="auth-switch">{isLogin ? 'New to Farmer to Customer?' : 'Already have an account?'} <button type="button" onClick={() => navigate(isLogin ? 'register' : 'login')}>{isLogin ? 'Create an account' : 'Log in'}</button></p>
      </div>
    </main>
  );
}

function ProtectedView({ user, expectedRole, navigate, onLogout }) {
  if (!user) {
    return (
      <main className="protected-page">
        <div className="protected-card">
          <p className="eyebrow"><span /> Account required</p>
          <h1>Log in to continue.</h1>
          <p>This area is available to registered {expectedRole}s.</p>
          <button className="auth-submit" type="button" onClick={() => navigate('login')}>Go to Login <ArrowRight size={17} /></button>
        </div>
      </main>
    );
  }

  if (user.role !== expectedRole) {
    return (
      <main className="protected-page">
        <div className="protected-card">
          <p className="eyebrow"><span /> Role restricted</p>
          <h1>This space is for {expectedRole}s.</h1>
          <p>Your current account is registered as a {user.role}.</p>
          <button className="auth-submit" type="button" onClick={() => navigate(user.role)}>Go to my space <ArrowRight size={17} /></button>
        </div>
      </main>
    );
  }

  return (
    <main className="protected-page">
      <div className="protected-card">
        <p className="eyebrow"><span /> Protected {expectedRole} area</p>
        <h1>Welcome, {user.full_name}.</h1>
        <p>Your {expectedRole} account is connected. Role-specific tools can be added here next.</p>
        <button className="auth-submit" type="button" onClick={onLogout}>Log out <ArrowRight size={17} /></button>
      </div>
    </main>
  );
}

function Marketplace() {
  const [selectedCategory, setSelectedCategory] = React.useState('All');
  const [cartItems, setCartItems] = React.useState([]);
  const visibleProducts = selectedCategory === 'All'
    ? products
    : products.filter((product) => product.category === selectedCategory);

  function addToCart(productName) {
    setCartItems((currentItems) => currentItems.includes(productName)
      ? currentItems
      : [...currentItems, productName]);
  }

  return (
    <section className="marketplace" id="products">
      <div className="section-heading">
        <div>
          <p className="eyebrow"><span /> From our farmers</p>
          <h2>Shop the <em>harvest.</em></h2>
        </div>
        <p className="section-description">Everything you need, grown with intention and delivered from a farm you can know.</p>
      </div>

      <div className="category-row" aria-label="Product categories">
        <button className={selectedCategory === 'All' ? 'category-card selected' : 'category-card'} type="button" onClick={() => setSelectedCategory('All')}>
          <span className="category-icon"><Leaf size={22} /></span>
          <span><strong>All products</strong><small>63 products</small></span>
        </button>
        {categories.map(({ icon: Icon, name, detail }) => (
          <button className={selectedCategory === name ? 'category-card selected' : 'category-card'} type="button" key={name} onClick={() => setSelectedCategory(name)}>
            <span className="category-icon"><Icon size={22} /></span>
            <span><strong>{name}</strong><small>{detail}</small></span>
          </button>
        ))}
      </div>

      <div className="catalog-heading">
        <p>{selectedCategory === 'All' ? 'Popular this week' : selectedCategory}</p>
        <span aria-live="polite"><ShoppingCart size={15} /> {cartItems.length} {cartItems.length === 1 ? 'item' : 'items'} in cart</span>
      </div>

      <div className="product-grid">
        {visibleProducts.map((product) => {
          const isAdded = cartItems.includes(product.name);
          return (
            <article className="product-card" key={product.name}>
              <div className="product-image-wrap">
                <img src={product.image} alt={product.name} loading="lazy" />
                <span className="product-category">{product.category}</span>
              </div>
              <div className="product-info">
                <div className="product-title-row"><h3>{product.name}</h3><span>{product.price}</span></div>
                <p className="farmer-name"><Leaf size={13} /> {product.farmer}</p>
                <button className={isAdded ? 'add-button added' : 'add-button'} type="button" onClick={() => addToCart(product.name)}>
                  {isAdded ? 'Added to Cart' : 'Add to Cart'} <ShoppingCart size={15} />
                </button>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

function Hero({ currentUser, navigate }) {
  return (
    <main>
      <section className="hero" id="home">
        <div className="hero-content">
          <p className="eyebrow"><span /> From the farm, with care</p>
          <h1>Fresh Products<br /><em>Directly from</em> Farmers.</h1>
          <p className="hero-copy">Discover the taste of local. We bring you honest, fresh produce from the farmers who grow it, so every purchase makes a difference.</p>
          <div className="hero-actions">
            <a className="button button-primary" href="#products">Shop Products <ArrowRight size={17} /></a>
            <a className="button button-secondary" href="#register?role=farmer" onClick={(event) => { event.preventDefault(); navigate('register?role=farmer'); }}>Join as Farmer <span className="button-plus">+</span></a>
          </div>
          <div className="hero-note"><Clock3 size={15} /> <span>Freshly harvested. Thoughtfully delivered.</span></div>
        </div>
        <div className="hero-visual" aria-label="A basket of fresh farm produce" role="img">
          <div className="sun-stamp"><span>GOOD<br />FOOD<br /><b>GROWS</b><br />HERE</span></div>
          <div className="produce-card produce-card-one"><span>01</span>Local harvest</div>
          <div className="produce-card produce-card-two"><span>24h</span>From soil to table</div>
          <div className="photo-credit">Grown nearby <span>•</span> Shared with care</div>
        </div>
      </section>

      <MarketplaceSection currentUser={currentUser} navigate={navigate} />

      <section className="feature-strip" id="about">
        <div className="feature-intro">
          <p className="eyebrow"><span /> Why choose us</p>
          <h2>Good food<br /><em>feels different.</em></h2>
        </div>
        <div className="feature-list">
          {features.map(({ icon: Icon, number, title, description }) => (
            <article className="feature" key={title}>
              <div className="feature-topline"><span className="feature-number">{number}</span><Icon size={25} strokeWidth={1.7} /></div>
              <h3>{title}</h3>
              <p>{description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="lower-band" id="join">
        <p>Better choices start close to home.</p>
        <a href="#products">Explore the harvest <ArrowRight size={17} /></a>
      </section>
    </main>
  );
}

function App() {
  const [menuOpen, setMenuOpen] = React.useState(false);
  const routeFromHash = () => window.location.hash.replace('#', '').split('?')[0] || 'home';
  const [route, setRoute] = React.useState(routeFromHash);
  const [currentUser, setCurrentUser] = React.useState(() => authStorage.getUser());
  const [authLoading, setAuthLoading] = React.useState(() => Boolean(authStorage.getToken()));

  React.useEffect(() => {
    const handleHashChange = () => setRoute(routeFromHash());
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  React.useEffect(() => {
    if (!authStorage.getToken()) {
      setAuthLoading(false);
      return undefined;
    }

    authApi.getCurrentUser()
      .then((response) => {
        setCurrentUser(response.data);
        authStorage.save(authStorage.getToken(), response.data);
      })
      .catch(() => {
        authStorage.clear();
        setCurrentUser(null);
      })
      .finally(() => setAuthLoading(false));
  }, []);

  function navigate(nextRoute) {
    window.location.hash = nextRoute;
    setMenuOpen(false);
  }

  function handleLogout() {
    authStorage.clear();
    setCurrentUser(null);
    navigate('home');
  }

  const isAuthRoute = route === 'login' || route === 'register';
  const registrationRole = new URLSearchParams(window.location.hash.split('?')[1] || '').get('role') === 'farmer' ? 'Farmer' : 'Customer';
  const orderSuccess = new URLSearchParams(window.location.hash.split('?')[1] || '').get('order') === 'success';

  return (
    <div className="app-shell">
      <Header menuOpen={menuOpen} setMenuOpen={setMenuOpen} currentUser={currentUser} onLogout={handleLogout} />
      {authLoading ? <main className="auth-loading">Checking your account...</main>
        : isAuthRoute ? <AuthPage mode={route} navigate={navigate} initialRole={registrationRole} onAuthenticated={setCurrentUser} />
          : route === 'customer' ? currentUser?.role === 'customer' ? <CustomerDashboard user={currentUser} navigate={navigate} orderSuccess={orderSuccess} /> : <ProtectedView user={currentUser} expectedRole="customer" navigate={navigate} onLogout={handleLogout} />
            : route === 'farmer-add-product' || route === 'farmer' ? currentUser?.role === 'farmer' ? <FarmerDashboard user={currentUser} navigate={navigate} addProductOnly={route === 'farmer-add-product'} /> : <ProtectedView user={currentUser} expectedRole="farmer" navigate={navigate} onLogout={handleLogout} />
              : <Hero currentUser={currentUser} navigate={navigate} />}
      <footer id="contact"><span>Farmer to Customer</span><span>Growing a closer food system.</span></footer>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
