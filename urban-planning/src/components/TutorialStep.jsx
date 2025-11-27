import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './TutorialStep.css'; 
const pasiTutorial = [
  {
    icon: '🗺️',
    titlu: 'Select a Neighborhood',
    descriere: "First, go to the Simulator page. You will see a map of Bucharest. Click on any of the highlighted neighborhoods (like 'Mărăști') to load its current data.",
  },
  {
    icon: '📊',
    titlu: "Analyze the 'Before' Data",
    descriere: "Once you select a neighborhood, a panel will appear showing the real-world data: Current Pollution levels, Land Use percentages (buildings, roads, green space), and other key metrics.",
  },
  {
    icon: '🎛️',
    titlu: 'Simulate a Change',
    descriere: "This is the 'what-if' part. Use the tools in the panel to make a change. For example, use a slider to 'decrease Buildings by 10%' and 'increase Green Space by 10%.'",
  },
  {
    icon: '💡',
    titlu: "See the 'After' Prediction",
    descriere: "As soon as you make a change, the AI model will run in the background. The 'Predicted Pollution' and other metrics will instantly update to show you the likely impact of your decision.",
  },
];

function Tutorial() {
  const [pasCurent, setPasCurent] = useState(0);

  const handleNext = () => {
    setPasCurent((prevPas) => Math.min(prevPas + 1, pasiTutorial.length - 1));
  };

  const handlePrev = () => {
    setPasCurent((prevPas) => Math.max(prevPas - 1, 0));
  };

  const ePrimulPas = pasCurent === 0;
  const eUltimulPas = pasCurent === pasiTutorial.length - 1;

  const pas = pasiTutorial[pasCurent];

  return (
    <div className="tutorial-page-background">
      <div className="tutorial-stepper">
        
        
        <h2 className="stepper-title">How to Use the Simulator</h2>
                
        <div className="stepper-progres">
          {pasiTutorial.map((_, index) => (
            <div
              key={index}
              className={`progres-dot ${index === pasCurent ? 'activ' : ''}`}
            />
          ))}
        </div>

        <div className="stepper-continut" key={pasCurent}>
          <div className="continut-icon">{pas.icon}</div>
          <h3>{pas.titlu}</h3>
          <p>{pas.descriere}</p>
        </div>

        <div className="stepper-navigatie">
          <button
            className="buton-stepper"
            onClick={handlePrev}
            disabled={ePrimulPas}
          >
            Prev
          </button>

          {!eUltimulPas ? (
           
            <button
              className="buton-stepper primar"
              onClick={handleNext}
            >
              Next
            </button>
          ) : (
           
            <Link
              to="/simulator" 
              className="buton-stepper primar cta-final"
            >
              Go to the simulator 
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}

export default Tutorial;