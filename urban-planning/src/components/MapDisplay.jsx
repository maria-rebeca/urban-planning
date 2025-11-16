import { MapContainer, TileLayer, GeoJSON } from "react-leaflet"
import "leaflet/dist/leaflet.css"
import geoJsonData from './../assets/UrbanAtlasBBox.json'
import { useState, useEffect } from 'react'
import MapClickHandler from "./MapClickHandler"

function getFeatureStyle(feature){
  const landClass = feature.properties.code_2018
  let fillColor = '#808080';
  
  switch(landClass){
    case "11100":
      fillColor = '#E60000'
      break;
    case "14100":
      fillColor = '#1bd618ff'
      break;
    case "13300":
      fillColor = '#e0bb19ff'
      break;
    case "50000":
      fillColor = '#00baf3ff'
      break;

  }

  return {
    fillColor: fillColor,   
    fillOpacity: 0.5,      
    color: 'transparent',   
    weight: 0               
  };
}


function MapDisplay({renderLandCover, renderLST}) {
  const [geeTileUrl, setGeeTileUrl] = useState(null);

  useEffect(() => {
    async function fetchGeeTileUrl() {
      try {
        const response = await fetch('http://localhost:5000/api/get-LST'); 
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.mapid) {
          const tileUrl = `https://earthengine.googleapis.com/v1/${data.mapid}/tiles/{z}/{x}/{y}`;

          setGeeTileUrl(tileUrl);
        } else {
          console.error("Error fetching GEE tiles:", data.error);
        }
      } catch (error) {
        console.error("Failed to fetch GEE tile URL:", error);
      }
    }

    fetchGeeTileUrl();
  }, []); 

  return (
    <>
      <MapContainer center={[44.439663, 26.096306]} zoom={13}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url='https://tile.openstreetmap.org/{z}/{x}/{y}.png'
        />

        
        {renderLandCover && <GeoJSON 
          data={geoJsonData}
          style={getFeatureStyle}
        />}

          {renderLST && geeTileUrl && (
            <TileLayer
              url={geeTileUrl} 
              attribution="Google Earth Engine"
              zIndex={10} 
              opacity={0.5}
            />
          )}
          <MapClickHandler/>
      </MapContainer>
    </>
  )
}

export default MapDisplay
