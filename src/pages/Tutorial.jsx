import React from 'react';
import TutorialStep from '../components/TutorialStep.jsx';

function Tutorial() {
  return (
    <div className="page-section">
      
      
      <TutorialStep
        number="1"
        title="Select a Neighborhood"
        startOpen={true}
        description="First, go to the Simulator page. You will see a map of Bucharest. Click on any of the highlighted neighborhoods (like 'Mărăști') to load its current data."
      />
      
    </div>
  );
}

export default Tutorial;