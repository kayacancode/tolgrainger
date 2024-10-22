import React, { useRef, useState, useEffect } from 'react';
import { MapContainer, TileLayer, FeatureGroup, useMap, LayersControl } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import html2canvas from 'html2canvas';
import ReactLeafletGoogleLayer from 'react-leaflet-google-layer';

const MapComponent = () => {
  const [area, setArea] = useState(null);
  const [polygon, setPolygon] = useState(null);
  const mapRef = useRef();

  const MapController = () => {
    const map = useMap();
    
    const captureArea = () => {
  if (map && polygon) {
    map.fitBounds(polygon.getBounds());
    
    setTimeout(() => {
      const mapElement = map.getContainer();
      const rect = mapElement.getBoundingClientRect();
      const options = {
        x: rect.left,
        y: rect.top,
        width: rect.width,
        height: rect.height,
        scale: window.devicePixelRatio
      };

      chrome.tabs.captureVisibleTab(null, options, function(dataUrl) {
        const link = document.createElement('a');
        link.href = dataUrl;
        link.download = 'map-area.png';
        link.click();
      });
    }, 2000); // Wait for 2 seconds after fitting bounds
  }
};

    return <button onClick={captureArea} style={{position: 'absolute', top: '10px', right: '10px', zIndex: 1000}}>Capture Area</button>;
  };

  const handleCreated = (e) => {
    const { layer } = e;
    setPolygon(layer);
    if (layer instanceof L.Polygon) {
      const areaInSquareMeters = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
      const areaInHectares = areaInSquareMeters / 10000;
      setArea(areaInHectares);
    }
  };

  return (
    <div>
      <MapContainer 
        center={[51.505, -0.09]} 
        zoom={13} 
        style={{ height: "400px", width: "100%" }}
        ref={mapRef}
      >
        <LayersControl position="topright">
          <LayersControl.BaseLayer checked name="OpenStreetMap">
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          </LayersControl.BaseLayer>
          <LayersControl.BaseLayer name="Google Satellite">
            <ReactLeafletGoogleLayer type={'satellite'} apiKey= "AIzaSyBK5b_glfw1-2g9RmK0-yk0oSUXaV0kJR8" />
          </LayersControl.BaseLayer>
        </LayersControl>
        <FeatureGroup>
          <EditControl
            position='topright'
            onCreated={handleCreated}
            draw={{
              rectangle: false,
              circle: false,
              circlemarker: false,
              marker: false,
              polyline: false,
            }}
          />
        </FeatureGroup>
        <MapController />
      </MapContainer>
      {area !== null && (
        <p>Area: {area.toFixed(4)} hectares ({(area * 2.47105).toFixed(4)} acres)</p>
      )}
    </div>
  );
};

export default MapComponent;