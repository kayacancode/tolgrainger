"use client";

import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import MapInput from "@/components/MapInput";

export default function HomePage() {
  const router = useRouter();

  const handleNext = () => {
    router.push("/input");
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      {/* <Sidebar /> */}

      {/* Main content */}
      <div className="flex-1 overflow-auto">
        <h1 className="text-lg font-bold text-center py-10">
          Draw your property lines
        </h1>
        <div className="h-full">
          <MapInput />
        </div>
        <div className="flex justify-end p-4">
          <button
            onClick={handleNext}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg text-lg"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
