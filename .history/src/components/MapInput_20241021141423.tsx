import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup } from 'react-leaflet';
import { EditControl } from 'react-leaflet-draw';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import html2canvas from 'html2canvas'; // Ensure this library is installed

const MapComponent = () => {
  const mapRef = useRef(null);
  const [polygon, setPolygon] = useState(null);
  const [area, setArea] = useState(0); // State to hold the area

  const onCreated = (e) => {
    const layer = e.layer;
    setPolygon(layer);

    // Calculate area in square meters and convert to acres
    const areaInSquareMeters = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
    setArea(areaInSquareMeters / 4046.86); // Convert to acres
  };

  const captureArea = async () => {
    if (!polygon) return;
  
    const bounds = polygon.getBounds();
    const map = mapRef.current;
  
    if (!map) {
      console.error("Map reference is not set");
      return;
    }
  
    // Fit the map to the bounds of the polygon
    map.fitBounds(bounds);
  
    // Allow some time for the map to render
    setTimeout(async () => {
      const container = map.getContainer();
  
      if (!container) {
        console.error("Container not found");
        return;
      }
  
      try {
        // Use html2canvas to capture the map area
        const canvas = await html2canvas(container, {
          backgroundColor: null, // Ensure transparency if needed
          scale: 2, // Increase scale for better resolution
          x: bounds.getWest(), // Capture starting point
          y: bounds.getSouth(),
          width: bounds.getEast() - bounds.getWest(), // Width based on bounds
          height: bounds.getNorth() - bounds.getSouth() // Height based on bounds
        });
  
        const img = canvas.toDataURL("image/png");
        const link = document.createElement('a');
        link.href = img;
        link.download = 'map-area.png';
        link.click();
      } catch (error) {
        console.error("Error capturing the area:", error);
      }
    }, 1000); // Wait for rendering
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
