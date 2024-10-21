import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup, useMap } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import html2canvas from 'html2canvas';

const MapComponent = () => {
  const [polygon, setPolygon] = useState(null);

  const onCreated = (e) => {
    setPolygon(e.layer);
  };

  const captureArea = () => {
    if (!polygon) return;

    const bounds = polygon.getBounds();
    // Create a new map instance to capture the bounds
    const map = L.map(document.createElement('div')).setView(bounds.getCenter(), 13);
    
    // Add the tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
    
    // Add the polygon to the temporary map
    polygon.addTo(map);

    // Wait for the map to render
    setTimeout(() => {
      html2canvas(map.getContainer()).then(canvas => {
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
      <MapContainer center={[40.6331, -89.3985]} zoom={13} style={{ height: "400px" }}>
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
