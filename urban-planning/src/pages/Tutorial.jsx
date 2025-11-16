import React from 'react';
import TutorialStep from '../components/TutorialStep.jsx';

function Tutorial() {
  return (
    <div className="page-section">
      <h1>How to Use the Simulator</h1>
      <p style={{maxWidth: '700px', margin: '0 auto 2rem auto'}}>
        Click on any step to expand and see the details.
      </p>
      
      <TutorialStep
        number="1"
        title="Select a Neighborhood"
        startOpen={true}
        description="First, go to the Simulator page. You will see a map of Bucharest. Click on any of the highlighted neighborhoods (like 'Mărăști') to load its current data."
      />
      
      <TutorialStep
        number="2"
        title="Analyze the 'Before' Data"
        description="Once you select a neighborhood, a panel will appear showing the real-world data: Current Pollution levels, Land Use percentages (buildings, roads, green space), and other key metrics."
      />

      <TutorialStep
        number="3"
        title="Simulate a Change"
        description="This is the 'what-if' part. Use the tools in the panel to make a change. For example, use a slider to 'decrease Buildings by 10%' and 'increase Green Space by 10%.'"
      />

      <TutorialStep
        number="4"
        title="See the 'After' Prediction"
        description="As soon as you make a change, the AI model will run in the background. The 'Predicted Pollution' and other metrics will instantly update to show you the likely impact of your decision."
      />
    </div>
  );
}

export default Tutorial;