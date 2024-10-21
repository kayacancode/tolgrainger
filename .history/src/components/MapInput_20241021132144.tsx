import React from 'react';
import { GoogleMap, DrawingManager } from '@react-google-maps/api';

export default function MapComponent = () => {
  const onPolygonComplete = (polygon) => {
    const area = google.maps.geometry.spherical.computeArea(polygon.getPath());
    console.log(`Area: ${area} square meters`);
  };

  return (
    <GoogleMap
      center={{ lat: 40.7128, lng: -74.0060 }}
      zoom={10}
    >
      <DrawingManager
        onPolygonComplete={onPolygonComplete}
        options={{
          drawingControl: true,
          drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: [google.maps.drawing.OverlayType.POLYGON],
          },
        }}
      />
    </GoogleMap>
  );
};