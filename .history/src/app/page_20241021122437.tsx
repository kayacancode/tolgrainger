"use client";

import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";

const MapComponent = dynamic(() => import("@/components/MapInput"), {
  ssr: false,
});

export default function HomePage() {
  const router = useRouter();

  const handleNext = () => {
    router.push("/input");
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Draw Your Property Boundaries</h2>
      <MapComponent />
      <button
        onClick={handleNext}
        className="bg-blue-500 text-white p-2 rounded"
      >
        Next
      </button>
    </div>
  );
}
