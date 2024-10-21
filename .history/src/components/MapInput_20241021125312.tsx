"use client"; // Mark this component as a client component

import { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Polyline, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css"; // Import Leaflet CSS
import L from "leaflet"; // Import Leaflet to fix marker icons

// Fix marker icons issue (necessary for Leaflet)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "/leaflet/images/marker-icon-2x.png",
  iconUrl: "/leaflet/images/marker-icon.png",
  shadowUrl: "/leaflet/images/marker-shadow.png",
});

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
  const mapRef = useRef<any>(null); // Reference to the map instance

  useEffect(() => {
    if (mapRef.current) {
      mapRef.current.setView([51.505, -0.09], 13); // Set initial view after the map is mounted
    }
  }, []);

  return (
    <div className="flex flex-col items-center space-y-4">
      <h1 className="text-2xl font-bold">Draw Your Property Boundaries</h1>

      {/* Set the map size */}
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

      <button
        className="mt-4 bg-green-500 hover:bg-green-700 text-white py-2 px-4 rounded"
        onClick={() => alert(JSON.stringify(positions))}
      >
        Next
      </button>
    </div>
  );
};

export default MapInput;
