"use client";


import { useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import axios from 'axios'

export default function CarbonInputPage() {
  const [credits, setCredits] = useState<number | "">("");
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    router.push("/result");
  };
  const handleNavigateToResults = () => {
    router.push('/results'); // Navigate to Results page
  };
  
  const handleRunScript = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:5000/run-script');
        console.log('Script result:', response.data);
    } catch (error) {
        console.error('Error running script:', error);
    }
};

  return (
    <form onSubmit={handleSubmit} className="space-y-4 text-center">
      <div className="flex">
        <Sidebar />
        <div className="block text-center items-center">
      <h2 className="text-2xl font-bold">Enter Carbon Credits</h2>
      <input
        type="number"
        placeholder="Requested Carbon Credits"
        value={credits}
        onChange={(e) => setCredits(e.target.value)}
        className=" p-2 border rounded"
      />
          <button onClick={handleRunScript} className="bg-green-500 text-white p-2 rounded">
      View Results
    </button>
      </div>
      </div>
    
    </form>
  );
}