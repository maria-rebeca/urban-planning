import { useMapEvents } from "react-leaflet";
function MapClickHandler({ isMarkerToolActive, handleMapClick }) {
    useMapEvents({
        click: (e) => {
            if (isMarkerToolActive) {
                handleMapClick(e.latlng); 
            }
        }
    });
    return null;
}

export default MapClickHandler;