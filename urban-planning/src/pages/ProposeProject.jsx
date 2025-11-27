import React, { useState } from 'react';
import './ProposeProject.css'; // Asigură-te că redenumești și fișierul CSS

function ProposeProject() {
  // 1. State to track if the form has been submitted
  const [isSubmitted, setIsSubmitted] = useState(false);

  // 2. State to hold the form data
  const [formData, setFormData] = useState({
    title: '',
    category: 'green-spaces', // Default value
    location: '',
    description: '',
  });

  // Function that updates state every time you type
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Function that runs on "Submit"
  const handleSubmit = (e) => {
    e.preventDefault(); // Stops the page from reloading

    // --- TH   IS IS WHERE YOU WILL ADD FIREBASE CODE LATER ---
    // For now, just log the data to the console
    console.log("Data that would be sent:", formData);
    // -------------------------------------------------

    // Set state to "submitted" to show the success message
    setIsSubmitted(true);
  };

  return (
    <div className="propunere-page-background">
      <div className="propunere-container">
        
        {/* Ternary "if": if NOT submitted, show the form */}
        {!isSubmitted ? (
          <>
            {/* --- THE FORM --- */}
            <h2 className="propunere-titlu">Have an idea for the city?</h2>
            <p className="propunere-subtitlu">
              Propose a new project, report an issue, or suggest an improvement.
            </p>
            
            <form onSubmit={handleSubmit} className="propunere-form">
              {/* Title Field */}
              <div className="form-grup">
                <label htmlFor="title">Proposal Title</label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="Ex: More benches in Central Park"
                  required
                />
              </div>
              
              {/* Category Field */}
              <div className="form-grup">
                <label htmlFor="category">Category</label>
                <select
                  id="category"
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  required
                >
                  <option value="green-spaces">Green Spaces & Parks</option>
                  <option value="transport">Transport & Mobility</option>
                  <option value="safety">Safety & Lighting</option>
                  <option value="infrastructure">Infrastructure & Potholes</option>
                  <option value="other">Other</option>
                </select>
              </div>

              {/* Location Field */}
              <div className="form-grup">
                <label htmlFor="location">Location (optional)</label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  placeholder="Ex: 123 Main St, near the playground"
                />
              </div>

              {/* Description Field */}
              <div className="form-grup">
                <label htmlFor="description">Describe your idea</label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows="5"
                  placeholder="Describe the problem or suggestion in detail..."
                  required
                ></textarea>
              </div>
              
              {/* Submit Button */}
              <button type="submit" className="buton-trimite">
                Submit Proposal
              </button>
            </form>
          </>
        ) : (
          <>
            {/* --- THE SUCCESS MESSAGE --- */}
            <div className="succes-mesaj">
              <div className="succes-icon">✅</div>
              <h2>Thank you for your proposal!</h2>
              <p>Your idea has been registered.</p>
              <button 
                onClick={() => setIsSubmitted(false)} 
                className="buton-succes-altul"
              >
                Submit another proposal
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default ProposeProject;