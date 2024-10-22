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
    <div className="">
                  <h1 className='text-lg font-bold text-center'>Draw your property lines</h1>

      <div className="h-screen  items-center justify-center">

      <MapInput />
      <button
        onClick={handleNext}
        className="bg-blue-500 text-white p-2 rounded"
      >
        Next
      </button>
      </div>
    </div>
  );
}
