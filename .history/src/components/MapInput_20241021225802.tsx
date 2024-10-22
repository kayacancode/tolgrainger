import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup, LayersControl } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import html2canvas from 'html2canvas';

const MapComponent = () => {
  const [area, setArea] = useState(null);
  const [polygon, setPolygon] = useState(null);
  const mapRef = useRef();

  const captureArea = () => {
    if (mapRef.current && polygon) {
      mapRef.current.fitBounds(polygon.getBounds());
  
      const checkTilesLoaded = () => {
        const container = mapRef.current.getContainer();
        const tilesLoaded = container.querySelectorAll('img.leaflet-tile-loaded').length > 0;
  
        if (tilesLoaded) {
          setTimeout(() => {
            html2canvas(container, {
              useCORS: true,
              allowTaint: true,
            }).then(canvas => {
              const img = canvas.toDataURL("image/png");
              const link = document.createElement('a');
              link.href = img;
              link.download = 'map-area.png';
              link.click();
            });
          }, 1000); // Delay to ensure rendering is complete
        } else {
          setTimeout(checkTilesLoaded, 500); // Retry after 500ms
        }
      };
  
      setTimeout(checkTilesLoaded, 2000); // Initial delay for panning
    }
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
  <div className="h-screen flex items-center justify-center bg-gray-100">
  <MapContainer 
    center={[51.505, -0.09]} 
    zoom={13} 
    style={{ height: "400px", width: "400px" }}
    ref={mapRef}
  >
    <LayersControl position="topright">
      <LayersControl.BaseLayer checked name="Mapbox Satellite">
        <TileLayer
          url="https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2anczMWQ2MDl6NzJycHhoNW82ZWI0ZyJ9.i3pzpTOdUqJSrK37pWMB3w"
          attribution="© Mapbox"
        />
      </LayersControl.BaseLayer>
    </LayersControl>
    <FeatureGroup>
      <EditControl
        position="topright"
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
    <button 
      onClick={captureArea} 
      className="absolute top-2 right-2 z-50 bg-blue-500 text-white px-4 py-2 rounded"
    >
      Capture Area
    </button>
  </MapContainer>
  {area !== null && (
    <p className="mt-4 text-center">
      Area: {area.toFixed(4)} hectares ({(area * 2.47105).toFixed(4)} acres)
    </p>
  )}
</div>

  );
};

export default MapComponent;