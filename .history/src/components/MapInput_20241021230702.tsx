import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup, LayersControl } from 'react-leaflet';
import { EditControl } from 'react-leaflet-draw';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import html2canvas from 'html2canvas';

const MapComponent = () => {
  const [area, setArea] = useState(null);
  const [polygon, setPolygon] = useState(null);
  const [coordinates, setCoordinates] = useState([]); // Store coordinates
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
            }).then((canvas) => {
              const img = canvas.toDataURL('image/png');
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
      // Store the coordinates of the polygon
      const latLngs = layer.getLatLngs()[0].map((latLng) => ({
        lat: latLng.lat,
        lng: latLng.lng,
      }));
      setCoordinates(latLngs);

      // Calculate area in hectares
      const areaInSquareMeters = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
      const areaInHectares = areaInSquareMeters / 10000;
      setArea(areaInHectares);
    }
  };

  return (
    <div className='h-screen  items-center justify-center'>
      <MapContainer
        center={[51.505, -0.09]}
        zoom={13}
        style={{ height: '400px', width: '400px' }}
        ref={mapRef}
      >
        <LayersControl position="topright">
          <LayersControl.BaseLayer checked name="Mapbox Satellite">
            <TileLayer
              url="https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2pvbmVzNDYiLCJhIjoiY20yanczMWQ2MDl6NzJycHhoNW82ZWI0ZyJ9.i3pzpTOdUqJSrK37pWMB3w"
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
          style={{ position: 'absolute', top: '10px', right: '10px', zIndex: 1000 }}
        >
          Capture Area
        </button>
      </MapContainer>
      {area !== null && (
        <p>
          Area: {area.toFixed(4)} hectares ({(area * 2.47105).toFixed(4)} acres)
        </p>
      )}
      {coordinates.length > 0 && (
        <div>
          <h3>Coordinates:</h3>
          <ul>
            {coordinates.map((coord, index) => (
              <li key={index}>
                Lat: {coord.lat.toFixed(6)}, Lng: {coord.lng.toFixed(6)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default MapComponent;
