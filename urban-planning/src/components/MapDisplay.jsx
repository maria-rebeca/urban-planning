import { MapContainer, TileLayer, GeoJSON } from "react-leaflet"
import "leaflet/dist/leaflet.css"
import { useState, useEffect, use } from 'react'
import MapClickHandler from "./MapClickHandler"

function MapDisplay({renderLandCover, renderLST}) {
  const [lstTileUrl, setLstTileUrl] = useState(null);
  const [landUseTileUrl, setLandUseTileUrl] = useState(null)

  useEffect(() => {
    async function fetchlstTileUrl() {
      try {
        const lstRes = await fetch('http://localhost:5000/api/get-LST'); 
        const lstData = await lstRes.json()
        if(lstData.mapid){
          setLstTileUrl(`https://earthengine.googleapis.com/v1/${lstData.mapid}/tiles/{z}/{x}/{y}`);
        }

        const luRes = await fetch('http://localhost:5000/api/get-landuse-tiles')
        const luData = await luRes.json()
        if(luData.mapid){
          setLandUseTileUrl(`https://earthengine.googleapis.com/v1/${luData.mapid}/tiles/{z}/{x}/{y}`);
        }
      }catch (error) {
        console.error("Failed to fetch GEE tile URL:", error);
      }
    }
    fetchlstTileUrl();
  }, []); 

  return (
    <>
      <MapContainer center={[44.439663, 26.096306]} zoom={13}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url='https://tile.openstreetmap.org/{z}/{x}/{y}.png'
        />
  
       {renderLandCover && landUseTileUrl && (
          <TileLayer
            url={landUseTileUrl}
            attribution="Urban Atlas (Copernicus)"
            zIndex={20} 
            opacity={0.5}
          />
        )}

        {renderLST && lstTileUrl && (
          <TileLayer
            url={lstTileUrl} 
            attribution="Google Earth Engine"
            zIndex={10} 
            opacity={1}
          />
        )}

        <MapClickHandler/>
      </MapContainer>
    </>
  )
}

export default MapDisplay
