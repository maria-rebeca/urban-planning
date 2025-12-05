import React, { useState, useCallback } from 'react';
import '../Simulator.css';
import MapDisplay from '../components/MapDisplay';
import MapMarkerTool from '../components/MapMarkerTool';
import axios from 'axios'; 

const cityData = {
  bucharest: {
    name: "Bucharest",
    position: [44.4268, 26.1025],
    zoom: 13
  },
  cluj: {
    name: "Cluj-Napoca",
    position: [46.7712, 23.6236],
    zoom: 14
  }
};

function Simulator() {
  const [selectedCity, setSelectedCity] = useState('bucharest');
  const [selectedTool, setSelectedTool] =useState('park');
  const [percentage, setPercentage] = useState(10);

  const [showLandUse, setShowLandUse] = useState(true); 
  const [showLST, setShowLST] = useState(true);

  const [isMarkerToolActive, setIsMarkerToolActive] = useState(false);
  const [markerPosition, setMarkerPosition] = useState(null);
  const [markerStats, setMarkerStats] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const currentCity = cityData[selectedCity];


  const handleCityChange = (event) => {
    setSelectedCity(event.target.value);
  };

  const handleToolChange = (event) => {
    setSelectedTool(event.target.value);
  };

  const handlePercentageChange = (event) => {
    setPercentage(event.target.value);
  };
  
  const handleClearMarker = useCallback(() => {
    setMarkerPosition(null);
    setMarkerStats(null);
    setIsLoading(false);
  }, []);

  const handleMarkerToolToggle = () => {
    const newState = !isMarkerToolActive;
    setIsMarkerToolActive(newState);
    if (!newState) {
      handleClearMarker();
    }
  };

  const fetchStats = useCallback(async (lat, lng) => {
    setIsLoading(true);
    setMarkerStats(null); 
    try {
      const response = await axios.get(`http://localhost:5000/api/get-stats?lat=${lat}&lng=${lng}`);
      setMarkerStats(response.data);
    } catch (error) {
      console.error("Eroare la preluarea statisticilor:", error);
      alert("A apărut o eroare la preluarea datelor statistice. Verifică serverul.");
      setMarkerPosition(null); 
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleMapClick = useCallback((latlng) => {
    if (isMarkerToolActive) {
      setMarkerPosition(latlng);
      fetchStats(latlng.lat, latlng.lng);
    }
  }, [isMarkerToolActive, fetchStats]);

  return (
    <div className="simulator-page">
      
      <div className="simulator-controls">
        <h2>Urban Simulator</h2>
        <p>Select your parameters to see their potential impact.</p>

        <div className="control-group">
          <label htmlFor="city-select">1. Select City:</label>
          <select id="city-select" value={selectedCity} onChange={handleCityChange}>
            <option value="bucharest">Bucharest</option>
            <option value="cluj">Cluj-Napoca</option>
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="tool-select">2. Select Land Use to Add:</label>
          <select id="tool-select" value={selectedTool} onChange={handleToolChange}>
            <option value="park">Green Park (Increases Green Space)</option>
            <option value="factory">Factory (Increases Industry)</option>
            <option value="house">Housing (Increases Buildings)</option>
            <option value="road">Road (Increases Roads)</option>
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="percentage-slider">3. Percentage of land to convert: {percentage}%</label>
          <input 
            id="percentage-slider" 
            type="range" 
            min="1" 
            max="100" 
            value={percentage} 
            onChange={handlePercentageChange} 
            className="slider"
          />
        </div>

        <div className="control-group">
            <MapMarkerTool 
                isActive={isMarkerToolActive}
                onToggle={handleMarkerToolToggle}
                markerData={markerStats} 
                onClearMarker={handleClearMarker} 
                isLoading={isLoading} 
            />
        </div>

        <button type="button" className="submit-btn">
          Run Simulation
        </button>
      </div>

      <MapDisplay 
        city={currentCity} 
        showLandUse={showLandUse} 
        showLST={showLST} 
        isMarkerToolActive={isMarkerToolActive}
        markerPosition={markerPosition} 
        handleMapClick={handleMapClick}
        markerStats={markerStats} 
        handleClearMarker={handleClearMarker} 
        isLoading={isLoading}
      />
      
    </div>
  )
}

export default Simulator