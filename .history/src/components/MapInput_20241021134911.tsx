import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';

const MapComponent = () => {
  const mapRef = useRef();
  const [polygon, setPolygon] = useState(null);

  const onCreated = (e) => {
    setPolygon(e.layer);
  };

  const captureArea = () => {
    if (!polygon) return;

    const map = mapRef.current.leafletElement;
    const bounds = polygon.getBounds();
    map.fitBounds(bounds);

    // Wait for the map to finish panning
    setTimeout(() => {
      html2canvas(document.querySelector(".leaflet-container")).then(canvas => {
        const img = canvas.toDataURL("image/png");
        const link = document.createElement('a');
        link.href = img;
        link.download = 'map-area.png';
        link.click();
      });
    }, 1000);
  };

  return (
    <div>
      <MapContainer ref={mapRef} center={[51.505, -0.09]} zoom={13} style={{ height: "400px" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <FeatureGroup>
          <EditControl
            position='topright'
            onCreated={onCreated}
            draw={{
              rectangle: false,
              circle: false,
              circlemarker: false,
              marker: false,
              polyline: false,
            }}
          />
        </FeatureGroup>
      </MapContainer>
      <button onClick={captureArea}>Capture Area</button>
    </div>
  );
};

export default MapComponent;