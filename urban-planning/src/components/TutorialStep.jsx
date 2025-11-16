import React, { useState } from 'react';
import './TutorialStep.css';

function TutorialStep(props) {
  const [isOpen, setIsOpen] = useState(props.startOpen || false);

  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="tutorial-step-card" onClick={toggleOpen}>
      <div className="step-number">{props.number}</div>
      <div className="step-content">
        <h3>{props.title}</h3>
        {isOpen && (
          <p>{props.description}</p>
        )}
      </div>
      <div className="step-toggle-icon">
        {isOpen ? '−' : '+'}
      </div>
    </div>
  );
}

export default TutorialStep;