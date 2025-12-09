import React, { useState, useCallback } from 'react';
import '../Simulator.css';
import MapDisplay from '../components/MapDisplay';
import MapMarkerTool from '../components/MapMarkerTool';
import axios from 'axios'; 

const LAND_USE_NAMES = {
  11100: "Continuous Urban Fabric",
  11210: "Discontinuous Dense Urban Fabric",
  11220: "Discontinuous Medium Urban Fabric",
  11230: "Discontinuous Low Density Urban",
  11240: "Discontinuous Very Low Density Urban",
  12100: "Industrial, Commercial, Public, Military and Private units",
  12210: "Fast transit Roads",
  12220: "Other Roads and associated land",
  12230: "Railways and associated land",
  12400: "Airports",
  13300: "Construction Sites",
  13400: "Land without current use",
  14100: "Green Urban Areas",
  14200: "Sports and Leisure Facilities",
  21000: "Arable land",
  22000: "Permanent crops",
  23000: "Pastures",
  24000: "Complex and mixed cultivations",
  31000: "Forests",
  32000: "Scrub and/or Herbaceous vegetation associations",
  33000: "Open spaces with little or no vegetation",
  40000: "Wetlands",
  50000: "Water Bodies"
};

const cityData = {
  bucharest: { name: "Bucharest", position: [44.4268, 26.1025], zoom: 13 },
  cluj: { name: "Cluj-Napoca", position: [46.7712, 23.6236], zoom: 14 }
};

function Simulator() {
  const [selectedCity, setSelectedCity] = useState('bucharest');
  const [selectedTool, setSelectedTool] = useState('14100'); 
  const [percentage, setPercentage] = useState(10);
  const [prediction, setPrediction] = useState(null);
  const [simulatedDist, setSimulatedDist] = useState(null)

  const [showLandUse, setShowLandUse] = useState(true); 
  const [showLST, setShowLST] = useState(false);

  const [isMarkerToolActive, setIsMarkerToolActive] = useState(false);
  const [markerPosition, setMarkerPosition] = useState(null);
  const [markerStats, setMarkerStats] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const currentCity = cityData[selectedCity];

  // --- SMART PRIORITY REPLACEMENT ---
  const calculateSmartDistribution = (currentDist, targetCode, percentageToAdd) => {
    let newDist = { ...currentDist };
    
    // Keep track of how much we still need to find
    let needed = parseFloat(percentageToAdd);

    const replaceOrder = [
      '13300', '13400', '33000', // Tier 1: Wasted
      '21000', '22000', '23000', '24000', // Tier 2: Agriculture
      '12100', '11240', '11230', // Tier 3: Low Density
      '11220', '11210', '11100', // Tier 4: High Density
      '14100', '14200', '31000', '32000', '12210', '12220' // Tier 5
    ];
    // Add targetCode to protected list so it's not shrunk in Step B
    const protectedCodes = ['50000', '40000', '31000', '12210', '12230', '12400', targetCode];

    // Step A: Priority List (Take from easiest first)
    for (const victimCode of replaceOrder) {
      if (needed <= 0) break;
      if (victimCode === targetCode) continue;

      if (newDist[victimCode] > 0) {
        const available = newDist[victimCode];
        if (available >= needed) {
          // Found enough space here
          newDist[victimCode] = available - needed;
          needed = 0;
        } else {
          // Take everything and keep looking
          newDist[victimCode] = 0;
          needed -= available;
        }
      }
    }

    // Step B: Fallback (Proportional Shrinkage)
    if (needed > 0) {
      // 1. Calculate total space available in non-protected categories
      const totalUnlocked = Object.keys(newDist)
        .filter(k => !protectedCodes.includes(k))
        .reduce((sum, k) => sum + (newDist[k] || 0), 0);

      if (totalUnlocked > 0) {
        // 2. 🔥 FIX: Don't take more than what's available
        const amountToTake = Math.min(needed, totalUnlocked);
        
        // 3. Calculate a positive shrinkage ratio
        // Example: If we have 20 and take 5, new total is 15. Ratio is 15/20 = 0.75
        const ratio = (totalUnlocked - amountToTake) / totalUnlocked;

        // 4. Apply shrinkage
        Object.keys(newDist).forEach(k => {
          if (!protectedCodes.includes(k)) {
            newDist[k] = newDist[k] * ratio;
          }
        });

        // 5. Update 'needed' to reflect what we couldn't find
        // If we needed 24 but only found 20, needed becomes 4.
        needed = needed - amountToTake;
      }
    }

    // Step C: Add the actual amount found to the target
    // If we wanted to add 34% but 'needed' is still 4%, we only add 30%.
    const actualAmountAdded = parseFloat(percentageToAdd) - needed;
    newDist[targetCode] = (newDist[targetCode] || 0) + actualAmountAdded;

    return newDist;
  };
  // --- SIMULATION RUNNER ---
  const runSimulation = async () => {
    if (!markerStats || !markerStats.land_use_dist) {
      alert("Please select a point on the map first!");
      return;
    }

    setIsLoading(true);
    setPrediction(null);

   try {
      const currentDist = {};
      const sourceDist = markerStats.land_use_dist; // <--- FIXED: Using your actual variable name

      sourceDist.forEach(item => {
        if (item.Code) {
          // Find the key that holds the percentage value (it's the key that isn't 'Code')
          const nameKey = Object.keys(item).find(k => k !== 'Code');
          const value = nameKey ? item[nameKey] : 0;
          
          // Map Code -> Value (e.g., "11100" -> 20.5)
          currentDist[String(item.Code)] = Number(value);
        }
      });

      const targetCode = String(selectedTool);
      const smartDist = calculateSmartDistribution(currentDist, targetCode, percentage);

      const total = Object.values(smartDist).reduce((a, b) => a + b, 0);
      const normalizedDist = {};
      
      // Ensure we send ALL known codes (even if 0) so the AI gets a full vector
      Object.keys(LAND_USE_NAMES).forEach(code => {
        const val = smartDist[code] || 0;
        normalizedDist[code] = total === 0 ? 0 : (val / total) * 100;
      });

      setSimulatedDist(normalizedDist)

      const response = await axios.post('http://localhost:5000/api/predict-temperature', {
        distribution: normalizedDist
      });

      if (response.data.status === 'success') {
        setPrediction(response.data.predicted_temp);
      } else {
        alert("Simulation Error: " + response.data.error);
      }

    } catch (error) {
      console.error("Simulation failed:", error);
      alert("Failed to connect to AI server.");
    } finally {
      setIsLoading(false);
    }
  };

  // --- FETCH STATS ---
  const fetchStats = useCallback(async (lat, lng) => {
    setIsLoading(true);
    setMarkerStats(null); 
    setPrediction(null);
    try {
      const response = await axios.get(`http://localhost:5000/api/get-stats?lat=${lat}&lng=${lng}`);
      let data = response.data;
      setMarkerStats(data);
      console.log(data)
    } catch (error) {
      console.error("Error fetching stats:", error);
      setMarkerPosition(null); 
    } finally {
      setIsLoading(false);
    }
  }, []);

  // --- EVENT HANDLERS ---
  const handleCityChange = (e) => setSelectedCity(e.target.value);
  const handleToolChange = (e) => setSelectedTool(e.target.value);
  const handlePercentageChange = (e) => setPercentage(e.target.value);
  
  const handleClearMarker = useCallback(() => {
    setMarkerPosition(null);
    setMarkerStats(null);
    setPrediction(null);
    setIsLoading(false);
  }, []);

  const handleMarkerToolToggle = () => {
    const newState = !isMarkerToolActive;
    setIsMarkerToolActive(newState);
    if (!newState) handleClearMarker();
  };

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
        {/* Map Layer Toggle Buttons */}
        <div className="control-group">
          <label>View Layer:</label>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              type="button"
              onClick={() => { setShowLandUse(true); setShowLST(false); }}
              style={{
                flex: 1,
                padding: '10px',
                borderRadius: '6px',
                border: '1px solid #ccc',
                backgroundColor: showLandUse ? '#4CAF50' : '#f5f5f5',
                color: showLandUse ? 'white' : '#333',
                cursor: 'pointer',
                fontWeight: 'bold',
                transition: 'all 0.2s'
              }}
            >
              🌍 Land Use
            </button>
            <button
              type="button"
              onClick={() => { setShowLandUse(false); setShowLST(true); }}
              style={{
                flex: 1,
                padding: '10px',
                borderRadius: '6px',
                border: '1px solid #ccc',
                backgroundColor: showLST ? '#FF5722' : '#f5f5f5',
                color: showLST ? 'white' : '#333',
                cursor: 'pointer',
                fontWeight: 'bold',
                transition: 'all 0.2s'
              }}
            >
              🌡️ Temperature
            </button>
          </div>
        </div>
        <div className="control-group">
          <label htmlFor="tool-select">2. Select Land Use to Add:</label>
          <select id="tool-select" value={selectedTool} onChange={handleToolChange}>
            <option disabled>──────────</option>
            {Object.entries(LAND_USE_NAMES).map(([code, name]) => (
               <option key={code} value={code}>{name}</option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="percentage-slider">3. Percentage to Add: {percentage}%</label>
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

        <button 
          type="button" 
          className="submit-btn" 
          onClick={runSimulation}
          disabled={isLoading || !markerStats}
          style={{ opacity: (!markerStats || isLoading) ? 0.6 : 1 }}
        >
          {isLoading ? "Simulating..." : "Run Simulation 🚀"}
        </button>

        {prediction !== null && (
          <div className="simulation-result" style={{ marginTop: '20px', padding: '15px', background: '#e3f2fd', borderRadius: '8px', borderLeft: '5px solid #2196f3' }}>
            <strong>Results:</strong>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px' }}>
              <span>Current LST:</span>
              <span>{markerStats?.mean_temp?.toFixed(2)}°C</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '5px', fontSize: '1.2em', color: '#1976d2', fontWeight: 'bold' }}>
              <span>Predicted LST:</span>
              <span>{prediction.toFixed(2)}°C</span>
            </div>
            <div style={{ fontSize: '0.9em', color: prediction > markerStats.mean_temp ? 'red' : 'green', marginTop: '5px', textAlign: 'right' }}>
              {prediction > markerStats.mean_temp ? "▲" : "▼"} {Math.abs(prediction - markerStats.mean_temp).toFixed(1)}°C change
            </div>
            {simulatedDist && (
              <div style={{ marginTop: '15px', borderTop: '1px solid #ccc', paddingTop: '10px' }}>
                <strong>New Land Distribution:</strong>
                <ul style={{ listStyle: 'none', paddingLeft: 0, marginTop: '5px', fontSize: '0.9em' }}>
                  {Object.entries(simulatedDist)
                    .filter(([code, pct]) => pct > 0.1) // Only show relevant items (>0.1%)
                    .sort((a, b) => b[1] - a[1])        // Sort by percentage Descending
                    .map(([code, pct]) => {
                      const name = LAND_USE_NAMES[code] || code;
                      const isTarget = String(code) === String(selectedTool);
                      return (
                        <li key={code} style={{ 
                          display: 'flex', 
                          justifyContent: 'space-between', 
                          marginBottom: '3px',
                          color: isTarget ? '#2196f3' : '#333',
                          fontWeight: isTarget ? 'bold' : 'normal'
                        }}>
                          <span>{name}:</span>
                          <span>{pct.toFixed(1)}%</span>
                        </li>
                      );
                    })}
                </ul>
              </div>
            )}
            <div style={{ fontSize: '0.8em', color: '#666', marginTop: '10px', fontStyle: 'italic' }}>
               *Simulated by replacing unused/empty land first.
            </div>
          </div>
        )}
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

export default Simulator;