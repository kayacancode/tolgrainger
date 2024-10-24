"use client";


import { useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";

export default function CarbonInputPage() {
  const [credits, setCredits] = useState<number | "">("");
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    router.push("/result");
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 text-center flex flex-col items-center">
    <h2 className="text-2xl font-bold mb-4">Enter Carbon Credits</h2>
    <div className="flex w-full max-w-md">
      <Sidebar />
      <div className="flex-1 ml-4">
        <input
          type="number"
          placeholder="Requested Carbon Credits"
          value={credits}
          onChange={(e) => setCredits(e.target.value)}
          className="p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
        />
      </div>
    </div>
    <button
      type="submit"
      className="bg-green-500 text-white p-2 rounded hover:bg-green-600 transition"
    >
      Submit
    </button>
  </form>
  
  );
}