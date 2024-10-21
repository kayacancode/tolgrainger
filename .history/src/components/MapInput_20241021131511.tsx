
import { useEffect, useState, useRef } from "react";
import { MapContainer,TileLayer, Polyline, useMapEvents, Marker,Popup } from "react-leaflet";


// Component for handling click events on the map
const MapClickHandler = ({ setPositions }: { setPositions: React.Dispatch<React.SetStateAction<number[][]>> }) => {
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      setPositions((prev) => [...prev, [lat, lng]]);
    },
  });
  return null; // This component does not render anything
};

const MapInput = () => {
  const [positions, setPositions] = useState<number[][]>([]);
  const mapRef = useRef<any>(null);
  const position = [51.505, -0.09]

  useEffect(() => {
    if (mapRef.current) {
      mapRef.current.setView([51.505, -0.09], 13); 
    }
  }, []);

  return (
    <div className="flex flex-col items-center space-y-4">
   <MapContainer
        ref={mapRef} // Attach the ref here
        className="w-full h-96 rounded-lg border-2 border-gray-300 shadow-lg"
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
        />
        <MapClickHandler setPositions={setPositions} /> {/* Pass setPositions to the handler */}
        <Polyline positions={positions} color="blue" />
      </MapContainer>
    </div>
  );
};

export default MapInput;
