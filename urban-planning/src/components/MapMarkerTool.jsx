import React from 'react';
import { FaMapPin, FaSpinner } from 'react-icons/fa'; 
import '../Simulator.css';

const MapMarkerTool = ({ isActive, onToggle, markerData, onClearMarker, isLoading }) => {
  return (
    <div className="tool-card">
      <div className="tool-header">
        <FaMapPin 
          className={`tool-icon ${isActive ? 'active' : ''}`} 
          onClick={onToggle} 
          title="Toggle Pin" 
        />
        <h3 className="tool-title">Point Analysis</h3>
      </div>
      <p className="tool-description">
        {isActive ? 'Click map to place pin.' : 'Click icon to activate.'}
      </p>

      {isLoading && <div className="marker-stats loading"><FaSpinner className="spinner"/> Loading...</div>}

      {!isLoading && markerData && (
        <div className="marker-stats">
          <h4>📍 Stats (1km Radius)</h4>
          <p>🌡️ **LST Temp:** {markerData.mean_temp} °C</p>
          
          <h5>Land Use Distribution:</h5>
          <ul>
            {markerData.land_use_dist && markerData.land_use_dist.map((item, index) => {
              const name = Object.keys(item).find(k => k !== 'Code');
              const value = item[name];
              
              if (!name) return null; // Safety skip
              return <li key={index}><strong>{name}:</strong> {Number(value).toFixed(1)}%</li>;
            })}
          </ul>
          <button onClick={onClearMarker} className="clear-btn">Clear Pin</button>
        </div>
      )}

      {!isLoading && isActive && !markerData && <div className="marker-stats empty">Select a location.</div>}
    </div>
  );
};

export default MapMarkerTool;