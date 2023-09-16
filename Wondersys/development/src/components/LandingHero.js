import React from 'react';
import './LandingHero.css';

function LandingHero() {
  return (
    <section className="landing-hero">
      <div className="container">
        <div className="content">
          <div className="text-content">
            <h1 className="title">Get Tech Ready with AVEVA</h1>
            <p className="paragraph">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed pellentesque arcu in ligula egestas, a vulputate massa mattis. 
            </p>
            <p className="paragraph">
              Nulla hendrerit tincidunt velit, ac tincidunt urna hendrerit non. Nulla at arcu nec urna ultrices facilisis.
            </p>
            <p className="paragraph">
              Etiam condimentum, urna non suscipit tincidunt, dui nisi luctus tortor, nec mattis est ante eu dui.
            </p>
            <p className="paragraph">
              Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Curabitur eget fringilla lectus.
            </p>
            <div className="buttons">
              <button className="button gray-button">Explore more</button>
              {/*<button className="button white-button">White Button</button>*/}
            </div>
          </div>
          <div className="image-content">
            <img className="hero-image" src="https://mir-s3-cdn-cf.behance.net/project_modules/fs/015ae485212519.5d7555aa1ebf8.jpg" alt="Hero" />
          </div>
        </div>
      </div>
    </section>
  );
}

export default LandingHero;
