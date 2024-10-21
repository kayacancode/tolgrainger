import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup, useMap } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import html2canvas from 'html2canvas';

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
          html2canvas(document.querySelector(".leaflet-container")).then(canvas => {
            const img = canvas.toDataURL("image/png");
            const link = document.createElement('a');
            link.href = img;
            link.download = 'map-area.png';
            link.click();
          });
        }, 1000); // Wait for map to finish panning
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
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
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