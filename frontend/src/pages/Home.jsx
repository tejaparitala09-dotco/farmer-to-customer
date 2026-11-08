import { Link } from 'react-router-dom';
import { ArrowRight, ShoppingBasket, Truck, Leaf, ShieldCheck, HeartHandshake } from 'lucide-react';

export default function Home() {
  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow light">A shorter journey from soil to table</span>
          <h1>
            Fresh From Farmers,<br />
            <em>Directly To You.</em>
          </h1>
          <p>
            Buy fresh vegetables, fruits, grains, and groceries directly from local growers.
            No middlemen, fair farmer compensation, and food at its peak flavour.
          </p>
          <div className="hero-actions">
            <Link className="button" to="/products">
              Shop Fresh Harvest <ArrowRight size={17} />
            </Link>
            <Link className="button ghost" to="/register">
              Join as Farmer
            </Link>
          </div>
        </div>
        <div className="hero-note">
          <span>01</span>
          <b>Harvested With Care</b>
          <small>Picked at sunrise, delivered straight to your doorstep.</small>
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Straight from the soil</span>
            <h2>Good food starts here.</h2>
          </div>
          <Link to="/products" className="text-link">
            View all produce <ArrowRight size={16} />
          </Link>
        </div>

        <div className="feature-grid">
          <div className="feature large">
            <div>
              <span className="eyebrow">01 / Fresh picks</span>
              <h3>
                Grown nearby.<br />
                Loved everywhere.
              </h3>
              <Link to="/products" className="text-link">
                Browse the harvest <ArrowRight size={16} />
              </Link>
            </div>
          </div>
          <div className="feature peach">
            <ShoppingBasket size={28} />
            <h3>
              Small farms,<br />
              big difference.
            </h3>
            <p>Every purchase supports rural communities and transparent farming.</p>
          </div>
          <div className="feature green">
            <Truck size={28} />
            <h3>
              From field<br />
              to doorstep.
            </h3>
            <p>Simple, direct logistics ensuring optimal freshness and minimal transit time.</p>
          </div>
        </div>
      </section>

      <section className="steps section">
        <div>
          <span className="eyebrow">The direct path</span>
          <h2>
            Good things,<br />
            <em>in five steps.</em>
          </h2>
        </div>
        <div className="step-list">
          {[
            'Farmers list seasonal crops & pricing',
            'Customers browse fresh produce & staples',
            'Orders placed with secure address details',
            'Farmers prepare, harvest & pack freshly',
            'Delivered directly to your home',
          ].map((step, idx) => (
            <div className="step" key={step}>
              <b>0{idx + 1}</b>
              <span>{step}</span>
              <ArrowRight size={17} />
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
