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
          title="Activează/Dezactivează Pinul" 
        />
        <h3 className="tool-title">Analiză Punctuală</h3>
      </div>
      <p className="tool-description">
        {isActive
          ? 'Pin activat. Fă clic pe hartă pentru a plasa un pin și a vedea statisticile din jur.'
          : 'Fă clic pe iconiță pentru a activa pinul și a analiza o zonă.'
        }
      </p>

      {/* Afișarea Datelor */}
      {isLoading && (
        <div className="marker-stats loading">
          <FaSpinner className="spinner" /> Se încarcă datele...
        </div>
      )}

      {!isLoading && markerData && (
        <div className="marker-stats">
          <h4>📍 Statistici Locație (Raza 1km)</h4>
          <p>🌡️ **Temperatura Medie (LST):** {markerData.mean_temp.toFixed(2)} °C</p>
          <h5>Procentaj Utilizare Teren:</h5>
          <ul>
            {markerData.land_use_dist.map((item, index) => {
              const [name, percentage] = Object.entries(item)[0];
              return (
                <li key={index}>
                  **{name}:** {percentage}%
                </li>
              );
            })}
          </ul>
          <button onClick={onClearMarker} className="clear-btn">Șterge Pinul</button>
        </div>
      )}

      {!isLoading && isActive && markerData === null && (
        <div className="marker-stats empty">
          Alege o locație pe hartă.
        </div>
      )}
    </div>
  );
};

export default MapMarkerTool;