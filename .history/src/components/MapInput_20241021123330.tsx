"use client"; // This line is critical for client components

import { useState } from "react";
import { MapContainer, TileLayer, Polyline, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css"; // Import Leaflet CSS

const MapInput = () => {
  const [positions, setPositions] = useState<number[][]>([]);

  // // Component to handle map events
  // const MapClickHandler = () => {
  //   useMapEvents({
  //     click(e) {
  //       const { lat, lng } = e.latlng;
  //       setPositions((prev) => [...prev, [lat, lng]]);
  //     },
  //   });
  //   return null; // Component doesn't render anything
  // };

  return (
    <div className="flex flex-col items-center space-y-4">
      <h1 className="text-2xl font-bold">Draw Your Property Boundaries</h1>

      {/* Ensure the map has a fixed height */}
      <MapContainer
        center={[51.505, -0.09]}
        zoom={13}
        className="w-full h-96 rounded-lg border-2 border-gray-300 shadow-lg"
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
        />
        {/* <MapClickHandler /> */}
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
