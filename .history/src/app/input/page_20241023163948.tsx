"use client";


import { useState } from "react";
import { useRouter } from "next/navigation";

export default function CarbonInputPage() {
  const [credits, setCredits] = useState<number | "">("");
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    router.push("/result");
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 text-center">
      <div className="flex">
      <h2 className="text-2xl font-bold">Enter Carbon Credits</h2>
      <input
        type="number"
        placeholder="Requested Carbon Credits"
        value={credits}
        onChange={(e) => setCredits(e.target.value)}
        className="w-full p-2 border rounded"
      />
      </div>
      <button type="submit" className="bg-green-500 text-white p-2 rounded">
        Submit
      </button>
    </form>
  );
}