"use client"
import React, { useState } from 'react';
import axios from 'axios';

const Results = () => {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleRunScript = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:5000/run-script');
      setResponse(res.data);  // Set the response from Flask
    } catch (err) {
      setError(err.message);  // Handle errors
      console.error("Error running script:", err);
    }
  };

  return (
    <div className="text-center p-6">
      <h1 className="text-2xl font-bold mb-4">Python Script Output</h1>
      <div>
        <button onClick={handleRunScript} className="mb-4 bg-blue-500 text-white p-2 rounded">
          Run Script
        </button>

        {error && <div className="text-red-500 mb-4">Error: {error}</div>}

        {response && response.plants && response.plants.length > 0 ? (
  <table className="min-w-full border border-gray-300">
    <thead>
      <tr className="bg-gray-200">
        <th className="border px-4 py-2">Plant</th>
        <th className="border px-4 py-2">Quantity</th>
        <th className="border px-4 py-2">Maturity</th>
      </tr>
    </thead>
    <tbody>
      {response.plants.map((plant, index) => (
        <tr key={index}>
          <td className="border px-4 py-2">{plant.name}</td>
          <td className="border px-4 py-2">{plant.quantity}</td>
          <td className="border px-4 py-2">{plant.maturity}</td>
        </tr>
      ))}
    </tbody>
  </table>
) : (
  <p>No plants found or response is not valid.</p>
)}

      </div>
    </div>
  );
};

export default Results;
