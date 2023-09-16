import React from 'react';

const footerStyle = {
  color: '#333',
  backgroundColor: '#f7f7f7',
  padding: '24px 0',
};

const containerStyle = {
  maxWidth: '1000px',
  maxHeight: '1000px',
  margin: '0 auto',
  display: 'flex',
  justifyContent: 'space-between',
};

const columnStyle = {
  flex: '1',
  marginRight: '20px',
};

const headingStyle = {
  fontSize: '16px',
  fontWeight: 'bold',
  marginBottom: '10px',
};

const linkStyle = {
  color: '#666',
  textDecoration: 'none',
  marginBottom: '6px',
  display: 'block',
};

const inputStyle = {
  padding: '6px',
  borderRadius: '4px',
  border: '1px solid #ccc',
  marginRight: '10px',
  width: '100%',
};

const buttonStyle = {
  padding: '6px 12px',
  borderRadius: '4px',
  backgroundColor: '#007bff',
  color: '#fff',
  border: 'none',
  cursor: 'pointer',
};

const paragraphStyle = {
  color: '#999',
  fontSize: '12px',
  textAlign: 'center',
};

const Footer = () => {
  return (
    <footer style={footerStyle}>
      <div style={containerStyle}>
        <div style={columnStyle}>
          <h2 style={headingStyle}>GET TO KNOW US</h2>
          <ul style={{ listStyle: 'none', padding: '0' }}>
            <li><a href="#" style={linkStyle}>About Us</a></li>
            <li><a href="#" style={linkStyle}>Contact Us</a></li>
            <li><a href="#" style={linkStyle}>Sitemap</a></li>
          </ul>
        </div>
        <div style={columnStyle}>
          <h2 style={headingStyle}>PRODUCTS</h2>
          <ul style={{ listStyle: 'none', padding: '0' }}>
            <li><a href="#" style={linkStyle}>Product - 1</a></li>
            <li><a href="#" style={linkStyle}>Product - 2</a></li>
            <li><a href="#" style={linkStyle}>Product - 3</a></li>
            <li><a href="#" style={linkStyle}>Product - 4</a></li>
          </ul>
        </div>
        <div style={columnStyle}>
          <h2 style={headingStyle}>TRAINING</h2>
          <ul style={{ listStyle: 'none', padding: '0' }}>
            <li><a href="#" style={linkStyle}>Course - 1</a></li>
            <li><a href="#" style={linkStyle}>Course - 2</a></li>
            <li><a href="#" style={linkStyle}>Course - 3</a></li>
            <li><a href="#" style={linkStyle}>Course - 4</a></li>
          </ul>
        </div>
        <div style={columnStyle}>
          <h2 style={headingStyle}>SUBSCRIBE</h2>
          <div style={{ display: 'flex', alignItems: 'flex-end', marginBottom: '10px' }}>
            <input type="text" placeholder="Email" style={inputStyle} />
            <button style={buttonStyle}>Join</button>
          </div>
          <p style={paragraphStyle}>Subscribe our blog for updates</p>
        </div>
      </div>
      <div style={{ backgroundColor: '#ccc', padding: '12px 0' }}>
        <div style={containerStyle}>
          <div>
            <a href="#" style={{ display: 'flex', alignItems: 'center', textDecoration: 'none', color: '#333' }}>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" className="w-10 h-10 p-2 bg-indigo-500 rounded-full" viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
              </svg>
              <span style={{ marginLeft: '10px', fontSize: '18px', fontWeight: 'bold' }}>WonderSys</span>
            </a>
          </div>
          <p style={{ color: '#999', fontSize: '12px', margin: '0' }}>© 2023 WonderSys — <a href="https://twitter.com/knyttneve" rel="noopener noreferrer" style={{ color: '#666', textDecoration: 'none' }} target="_blank">@wondersys</a></p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
