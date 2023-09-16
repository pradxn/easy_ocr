import React from 'react';
import './Products.css';

const Products = () => {
  return (
    <section className="products-section">
      <div className="container">
        <div className="heading">
          <h1>Our Products</h1>
          <div className="products-container">
          <Product
            imageSrc="https://www.aveva.com/en/training/cloud-training-center/_jcr_content/root/main_container/main-container/responsivegrid/background_container/backgroundCon/column_control/2colpar1/image/.coreimg.png/1690371312366/aveva-e3d-design-model-600x450.png"
            title="Shooting Stars"
            description="Swag shoivdigoitch literally meditation subway tile tumblr cold-pressed. Gastropub street art beard dreamcatcher neutra, ethical XOXO lumbersexual."
          />
          <Product
            imageSrc="https://www.aveva.com/en/training/cloud-training-center/_jcr_content/root/main_container/main-container/responsivegrid/background_container/backgroundCon/column_control/2colpar1/image/.coreimg.png/1690371312366/aveva-e3d-design-model-600x450.png"
            title="The Catalyzer"
            description="Swag shoivdigoitch literally meditation subway tile tumblr cold-pressed. Gastropub street art beard dreamcatcher neutra, ethical XOXO lumbersexual."
          />
          <Product
            imageSrc="https://www.aveva.com/en/training/cloud-training-center/_jcr_content/root/main_container/main-container/responsivegrid/background_container/backgroundCon/column_control/2colpar1/image/.coreimg.png/1690371312366/aveva-e3d-design-model-600x450.png"
            title="The 400 Blows"
            description="Swag shoivdigoitch literally meditation subway tile tumblr cold-pressed. Gastropub street art beard dreamcatcher neutra, ethical XOXO lumbersexual."
          />
        </div>
        </div>
      </div>
    </section>
  );
}

const Product = ({ imageSrc, title, description }) => {
  return (
    <div className="product">
      <div className="product-image">
        <img src={imageSrc} alt={title} />
      </div>
      <h2 className="product-title">{title}</h2>
      <p className="product-desc">{description}</p>
      <button className="product-button">Learn More</button>
    </div>
  );
}

export default Products;
