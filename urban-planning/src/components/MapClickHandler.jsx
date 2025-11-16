import { useMapEvents } from "react-leaflet";
function MapClickHandler(){
   useMapEvents({
    click: async (e) => {
        const {lat, lng} = e.latlng
        try{
            const response = await fetch(`http://localhost:5000/api/get-stats?lat=${lat}&lng=${lng}`)
            const data = await response.json()
            console.log(data)
        }catch(error){
            console.error("Error stats:", error)
        }
    }
   })
   return null
}

export default MapClickHandler