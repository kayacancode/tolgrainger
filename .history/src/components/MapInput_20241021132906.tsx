import React, { useState } from 'react';
import { MapContainer, TileLayer, FeatureGroup } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";

const MapComponent = () => {
  const [area, setArea] = useState(null);

  const _onCreate = (e) => {
    const { layer } = e;
    const area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
    setArea(area);
  };

  return (
    <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: "400px", width: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <FeatureGroup>
        <EditControl
          position='topright'
          onCreated={_onCreate}
          draw={{
            rectangle: false,
            circle: false,
            circlemarker: false,
            marker: false,
            polyline: false,
          }}
        />
      </FeatureGroup>
      {area && <p>Area: {area.toFixed(2)} square meters</p>}
    </MapContainer>
  );
};

export default MapComponent;