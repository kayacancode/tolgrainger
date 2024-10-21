import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup, useMap } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import html2canvas from 'html2canvas';

// Custom hook to get the map instance
const useMapInstance = () => {
  const map = useMap();
  return map;
};

const MapComponent = () => {
  const mapRef = useRef(null); // Reference for the MapContainer
  const [polygon, setPolygon] = useState(null);

  const onCreated = (e) => {
    setPolygon(e.layer);
  };

  const captureArea = () => {
    if (!polygon) return; // Ensure polygon is defined

    const bounds = polygon.getBounds();
    
    // Fit the map to the bounds of the polygon
    const map = mapRef.current; // Get the current map reference
    map.fitBounds(bounds);

    // Allow time for the map to render
    setTimeout(() => {
      html2canvas(mapRef.current.getContainer(), {
        useCORS: true, // Enable CORS to capture external images
      }).then(canvas => {
        const img = canvas.toDataURL("image/png");
        const link = document.createElement('a');
        link.href = img;
        link.download = 'map-area.png';
        link.click();
      }).catch((error) => {
        console.error("Error capturing the map: ", error);
      });
    }, 1000);
  };

  return (
    <div>
      <MapContainer ref={mapRef} center={[40.6331, -89.3985]} zoom={13} style={{ height: "400px" }}>
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
