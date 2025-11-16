import React from 'react';
import { Link } from 'react-router-dom';
import homePageImage1 from '../assets/papers_on_table.jpg';
import homePageImage2 from '../assets/building_construction.jpg';
import homePageImage3 from '../assets/urban_pollution.jpg';

function Home() {
  return (
    <div>
      <div className="page-section">
        <h1>Welcome to the Urban AI Simulator</h1>
        <p>
          See how urban planning decisions impact the state of the environment in just a few steps!
        </p>
        <h5>Check out the <Link to="/tutorial">tutorial</Link> section first</h5>
      </div>

    <div className="image-gallery">
          <img 
            src={homePageImage1} 
            alt="Urban planning papers on a table" 
            className="gallery-image" 
          />
          <img 
            src={homePageImage2} 
            alt="Building construction site" 
            className="gallery-image" 
          />
          <img 
            src={homePageImage3} 
            alt="City with urban pollution" 
            className="gallery-image" 
          />
        </div>

      <div className="page-section contact-section">
        <h2>Get in Touch</h2>
        <p>We'd love to hear from you. Send us a message!</p>
        
        <form className="contact-form">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input type="text" id="name" name="name" required />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input type="email" id="email" name="email" required />
          </div>

          <div className="form-group">
            <label htmlFor="message">Message</label>
            <textarea id="message" name="message" rows="5" required></textarea>
          </div>

          <button type="submit" className="submit-btn">Send Message</button>
        </form>
      </div>

    </div>
  );
}

export default Home;