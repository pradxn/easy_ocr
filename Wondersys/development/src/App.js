import React, { useState } from 'react';
import './App.css';
import logoImage from './images/WonderSys.png';

import LandingHero from './components/LandingHero'
/*import VideoComp from './components/VideoComp';*/
import Products from './components/Products';
import Clients from './components/Clients';
import Footer from './components/Footer';

function App() {
  const [isMenuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!isMenuOpen);
  };

  const navigationLinks = ['Products', 'Services', 'Training', 'Clients', 'About Us', ''];

  return (
    <>
    <header className={`header ${isMenuOpen ? 'mobile-menu-open' : ''}`}>
      <div className="logo-container">
        <img src={logoImage} alt="Company Logo" className="logo-image" />
        <h1 className="logo">WonderSys</h1>
      </div>
      <nav className={`nav ${isMenuOpen ? 'open' : ''}`}>
        <ul className={`nav-list ${isMenuOpen ? 'mobile-mode' : ''}`}>
          {navigationLinks.map((link, index) => (
            <li key={index} className="nav-item">
              {isMenuOpen ? <h4>{link}</h4> : <a href={`#${link.toLowerCase().replace(' ', '-')}`}>{link}</a>}
            </li>
          ))}
        </ul>
      </nav>
      <div className={`mobile-menu-icon ${isMenuOpen ? 'open' : ''}`} onClick={toggleMenu}>
        <div className="bar"></div>
        <div className="bar"></div>
        <div className="bar"></div>
      </div>
      <button className={`contact-btn ${isMenuOpen ? 'hidden' : ''}`}>Book a call</button>
    </header>
    
    <div>
      <LandingHero />
    </div>

    {/*<div>
      <br />
    </div>

    <div>
      <VideoComp />
          </div>

    <div>
      <br />
    </div>*/}

    <div>
      <Products />
    </div>

    <div>
      <Clients />
    </div>

    <div>
      <Footer />
    </div>

    </>
  );
}

export default App;