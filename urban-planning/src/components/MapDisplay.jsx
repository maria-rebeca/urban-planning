import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet"
import "leaflet/dist/leaflet.css"
import { useState, useEffect, useCallback } from 'react'
import MapClickHandler from "./MapClickHandler"
import '../Simulator.css';
import axios from 'axios';

function MapDisplay({ 
    city, 
    showLandUse, 
    showLST, 
    isMarkerToolActive, 
    markerPosition, 
    handleMapClick, 
    markerStats, 
    handleClearMarker, 
    isLoading 
}) {
  const [lstTileUrl, setLstTileUrl] = useState(null);
  const [landUseTileUrl, setLandUseTileUrl] = useState(null);

  const renderMarker = () => {
    if (!markerPosition) return null;

    return (
        <Marker position={markerPosition}>
            <Popup>
                {isLoading ? (
                    <div>Se încarcă datele...</div>
                ) : markerStats ? (
                    <div>
                        **Lat: {markerPosition.lat.toFixed(4)}, Lng: {markerPosition.lng.toFixed(4)}**
                        <p>🌡️ **Temp. Medie:** {markerStats.mean_temp.toFixed(2)} °C</p>
                        <p> **Distribuție:**</p>
                        <ul>
                            {markerStats.land_use_dist.map((item, index) => {
                                const [name, percentage] = Object.entries(item)[0];
                                return (
                                    <li key={index}>
                                        *{name}:* {percentage}%
                                    </li>
                                );
                            })}
                        </ul>
                        <button onClick={handleClearMarker}>Șterge Pinul</button>
                    </div>
                ) : (
                    <div>A apărut o eroare la încărcarea datelor.</div>
                )}
            </Popup>
        </Marker>
    );
  };

  useEffect(() => {
    async function fetchGeeTileUrls() {
      try {
        const lstRes = await axios.get('http://localhost:5000/api/get-LST'); 
        if(lstRes.data.mapid){
          setLstTileUrl(`https://earthengine.googleapis.com/v1/${lstRes.data.mapid}/tiles/{z}/{x}/{y}`);
        }

        const luRes = await axios.get('http://localhost:5000/api/get-landuse-tiles');
        if(luRes.data.mapid){
          setLandUseTileUrl(`https://earthengine.googleapis.com/v1/${luRes.data.mapid}/tiles/{z}/{x}/{y}`);
        }
      }catch (error) {
        console.error("Failed to fetch GEE tile URL:", error);
      }
    }
    fetchGeeTileUrls();
  }, []); 

  const initialCenter = city.position || [44.439663, 26.096306];
  const initialZoom = city.zoom || 13;

  return (
    <div className="map-container">
      <MapContainer center={initialCenter} zoom={initialZoom} key={city.name}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url='https://tile.openstreetmap.org/{z}/{x}/{y}.png'
        />
 
        {showLandUse && landUseTileUrl && (
          <TileLayer
            url={landUseTileUrl}
            attribution="Urban Atlas (Copernicus)"
            zIndex={20} 
            opacity={0.5}
          />
        )}

        {showLST && lstTileUrl && (
          <TileLayer
            url={lstTileUrl} 
            attribution="Google Earth Engine"
            zIndex={10} 
            opacity={0.5}
          />
        )}

        <MapClickHandler 
            isMarkerToolActive={isMarkerToolActive} 
            handleMapClick={handleMapClick}
        />

        {renderMarker()}
      </MapContainer>
    </div>
  )
}

export default MapDisplay;