import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import L from 'leaflet';

const MapComponent = () => {
  const mapRef = useRef(null);
  const [polygon, setPolygon] = useState(null);
  const [area, setArea] = useState(0); // State to hold the area

  const onCreated = (e) => {
    const layer = e.layer;
    setPolygon(layer);
    
    // Calculate area in square meters and convert to acres (1 acre = 4046.86 square meters)
    const areaInSquareMeters = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
    setArea(areaInSquareMeters / 4046.86); // Convert to acres
  };

  const captureArea = () => {
    if (!polygon) return;

    const bounds = polygon.getBounds();
    const map = mapRef.current; // Get the current map reference
    map.fitBounds(bounds);

    // Wait for the map to render
    setTimeout(() => {
      // Create a new canvas
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');

      // Set canvas dimensions based on bounds
      const topLeft = map.latLngToContainerPoint(bounds.getNorthWest());
      const bottomRight = map.latLngToContainerPoint(bounds.getSouthEast());
      
      const width = bottomRight.x - topLeft.x;
      const height = bottomRight.y - topLeft.y;
      
      canvas.width = width;
      canvas.height = height;

      // Draw the map area onto the canvas
      context.drawImage(
        mapRef.current.getContainer(),
        topLeft.x, topLeft.y,
        width, height,
        0, 0,
        width, height
      );

      const img = canvas.toDataURL("image/png");
      const link = document.createElement('a');
      link.href = img;
      link.download = 'map-area.png';
      link.click();
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
      <div>
        {polygon && <p>Area: {area.toFixed(2)} acres</p>}
      </div>
      <button onClick={captureArea}>Capture Area</button>
    </div>
  );
};

export default MapComponent;
