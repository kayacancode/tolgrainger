"use client";

import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";

import MapInput from "@/components/MapInput";

export default function HomePage() {
  const router = useRouter();

  const handleNext = () => {
    router.push("/input");
  };

  return (
    <div className="space-y-6">
      <MapInput />
      <button
        onClick={handleNext}
        className="bg-blue-500 text-white p-2 rounded"
      >
        Next
      </button>
    </div>
  );
}
