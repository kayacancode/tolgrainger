"use client";

import { useState } from "react";
import dynamic from "next/dynamic";

const MapWithTrees = dynamic(() => import("@/components/MapWithTrees"), {
  ssr: false,
});

export default function ResultPage() {
  const [treeCount, setTreeCount] = useState(100);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Tree Planting Results</h2>
      <MapWithTrees treeCount={treeCount} />
      <input
        type="range"
        min="0"
        max="500"
        value={treeCount}
        onChange={(e) => setTreeCount(+e.target.value)}
        className="w-full"
      />
      <p>Projected Carbon Sequestration: {treeCount * 0.1} tons/year</p>
    </div>
  );
}
