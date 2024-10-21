// pages/index.tsx
import MapComponent from "../components/MapComponent";
import { useState } from "react";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();
  const [polygonData, setPolygonData] = useState<number[][]>([]);

  const handlePolygonDrawn = (polygon: number[][]) => {
    setPolygonData(polygon);
    router.push({
      pathname: "/carbon-input",
      query: { polygon: JSON.stringify(polygon) },
    });
  };

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold mb-5">Draw Your Property</h1>
      <p>Click to add points. Double-click to complete the boundary.</p>
      <MapComponent onPolygonDrawn={handlePolygonDrawn} />
    </div>
  );
}
