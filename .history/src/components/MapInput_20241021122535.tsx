"use client";

import { useState } from "react";
import { MapContainer, TileLayer, Polyline, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const MapInput = () => {
  const [positions, setPositions] = useState<number[][]>([]);

  // This function must be inside a child of MapContainer
  const MapClickHandler = () => {
    useMapEvents({
      click(e) {
        const { lat, lng } = e.latlng;
        setPositions((prev) => [...prev, [lat, lng]]);
      },
    });

    return null; // Component renders nothing
  };

  return (
    <MapContainer center={[51.505, -0.09]} zoom={13} className="h-96">
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <MapClickHandler />
      <Polyline positions={positions} color="blue" />
    </MapContainer>
  );
};

export default MapInput;
