import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup, LayersControl } from 'react-leaflet';
import { EditControl } from 'react-leaflet-draw';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import html2canvas from 'html2canvas';

const MapComponent = () => {
  const [area, setArea] = useState<number | null>(null);
  const [polygon, setPolygon] = useState<L.Polygon | null>(null);
  const [coordinates, setCoordinates] = useState<{ lat: number; lng: number }[]>([]);
  const [popupVisible, setPopupVisible] = useState(false); // State for popup visibility
  const mapRef = useRef<L.Map | null>(null);

  const captureArea = () => {
    if (mapRef.current && polygon) {
      mapRef.current.fitBounds(polygon.getBounds());

      const checkTilesLoaded = () => {
        const container = mapRef.current!.getContainer();
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

  const handleCreated = (e: any) => {
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
      setPopupVisible(true); // Show popup when area is calculated
    }
  };

  return (
    <div className='relative'>
      {/* Popup for area and coordinates */}
      {popupVisible && (
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-white shadow-md rounded p-4 z-10">
          <h3 className="font-bold">Area and Coordinates</h3>
          {area !== null && (
            <p>
              Area: {area.toFixed(4)} hectares ({(area * 2.47105).toFixed(4)} acres)
            </p>
          )}
          {coordinates.length > 0 && (
            <div>
              <h4 className="font-semibold">Coordinates:</h4>
              <ul>
                {coordinates.map((coord, index) => (
                  <li key={index}>
                    Lat: {coord.lat.toFixed(6)}, Lng: {coord.lng.toFixed(6)}
                  </li>
                ))}
              </ul>
            </div>
          )}
          <button
            className="mt-2 text-red-500"
            onClick={() => setPopupVisible(false)}
          >
            Close
          </button>
        </div>
      )}

      <MapContainer
        center={[41.8780, -93.0977]}
        zoom={13}
        style={{ height: '1000px', width: '100%' }}
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
      </MapContainer>
    </div>
  );
};

export default MapComponent;
