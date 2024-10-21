// components/MapComponent.tsx
import { MapContainer, TileLayer, Polygon, useMapEvents } from "react-leaflet";
import { useState } from "react";
import "leaflet/dist/leaflet.css";

const MapComponent = ({ onPolygonDrawn }: { onPolygonDrawn: (polygon: any) => void }) => {
  const [positions, setPositions] = useState<number[][]>([]);

  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      setPositions((prev) => [...prev, [lat, lng]]);
    },
    dblclick() {
      onPolygonDrawn(positions);
    },
  });

  return (
    <MapContainer
      center={[37.7749, -122.4194]}
      zoom={13}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {positions.length > 1 && <Polygon positions={positions} />}
    </MapContainer>
  );
};

export default MapComponent;
