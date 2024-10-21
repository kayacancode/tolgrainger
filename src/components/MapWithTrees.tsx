"use client";

import { MapContainer, TileLayer, Marker } from "react-leaflet";

export default function MapWithTrees({ treeCount }: { treeCount: number }) {
  const markers = Array.from({ length: treeCount }).map((_, index) => (
    <Marker key={index} position={[51.505 + index * 0.001, -0.09]} />
  ));

  return (
    <MapContainer center={[51.505, -0.09]} zoom={13} className="h-96">
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {markers}
    </MapContainer>
  );
}
