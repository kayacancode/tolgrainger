"use client";

import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";

import MapInput from "@/components/MapInput";
import Sidebar from "@/components/SideBar";

export default function HomePage() {
  const router = useRouter();

  const handleNext = () => {
    router.push("/input");
  };

  return (
    <div className="flex">
      <Sidebar />
                  <h1 className='text-lg font-bold text-center py-10'>Draw your property lines</h1>


      <MapInput />
      <div className="float-right p-10 justify-center ">
      <button
        onClick={handleNext}
        className="bg-blue-500 text-white p-2 rounded  text-lg text-center"
      >
        Next
      </button>
      </div>
    </div>
  );
}
