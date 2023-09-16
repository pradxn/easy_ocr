import React from 'react';
import './Clients.css';

const Client = ({ imageSrc, review, companyName }) => {
  return (
    <div className="client">
      <div className="client-image">
        <img src={imageSrc} alt={`Client ${companyName}`} />
      </div>
      <div className="client-reviews-container">
        <p className="client-review">
          {review}
        </p>
      </div>
      <p className="client-name">{companyName}</p>
      <button className="client-button">Learn More</button>
    </div>
  );
};

const Clients = () => {
  const clientData = [
    {
      imageSrc: "https://s3.us-east-1.amazonaws.com/cdn.designcrowd.com/blog/starbucks-logo-through-the-years/aaaa.png",
      review: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris aliquam tellus vel tellus lobortis, a tincidunt odio hendrerit.",
      companyName: "Company A"
    },
    {
      imageSrc: "https://s3.us-east-1.amazonaws.com/cdn.designcrowd.com/blog/starbucks-logo-through-the-years/aaaa.png",
      review: "Vivamus convallis urna eget lobortis. Sed non magna a eros varius suscipit. Nulla facilisi.",
      companyName: "Company B"
    },
    {
      imageSrc: "https://s3.us-east-1.amazonaws.com/cdn.designcrowd.com/blog/starbucks-logo-through-the-years/aaaa.png",
      review: "Praesent aliquet vehicula eros, ut tincidunt justo vestibulum vel. Proin tincidunt, mi id luctus volutpat, dolor velit auctor dolor.",
      companyName: "Company C"
    }
  ];

  return (
    <section className="clients-section">
      <div className="container">
        <div className="heading">
          <h2>Client Reviews</h2>
          <div className="clients-container">
            {clientData.map((client, index) => (
            <Client
              key={index}
              imageSrc={client.imageSrc}
              review={client.review}
              companyName={client.companyName}
              />
              ))}
        </div>
        </div>
      </div>
    </section>
  );
};

export default Clients;
