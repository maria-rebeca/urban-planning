import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import '../Simulator.css'

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

  return (
    <div>
      
      <div className="page-section simulator-controls">
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
          <label htmlFor="percentage-slider">
            3. Percentage of land to convert: <strong>{percentage}%</strong>
          </label>
          <input
            type="range"
            id="percentage-slider"
            min="1"
            max="100"
            value={percentage}
            onChange={handlePercentageChange}
            className="slider"
          />
        </div>

        <button type="button" className="submit-btn">
          Run Simulation
        </button>

      </div>

      <MapContainer 
        key={selectedCity} 
        center={currentCity.position} 
        zoom={currentCity.zoom}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={currentCity.position}>
          <Popup>{currentCity.name}</Popup>
        </Marker>
      </MapContainer>
      
    </div>
  )
}

export default Simulator