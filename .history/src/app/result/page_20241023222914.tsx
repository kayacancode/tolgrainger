// Results.tsx
"use client"
import React, { useState } from 'react';

const Results = () => {
  const [output, setOutput] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchPythonOutput = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/run-script/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: "Your input data here" }),
      });

      const result = await response.json();
      if (result.error) {
        setError(result.error);
      } else {
        setOutput(result.output);
      }
    } catch (err) {
      setError('Failed to connect to backend');
    }
  };

  return (
    <div className="text-center p-6">
      <h1 className="text-2xl font-bold mb-4">Python Script Output</h1>
      <button
        onClick={fetchPythonOutput}
        className="bg-blue-500 text-white p-2 rounded mb-4"
      >
        Run Python Script
      </button>

      {output && (
        <div className="bg-gray-100 p-4 rounded shadow">
          <h3 className="text-lg font-bold">Output:</h3>
          <pre>{output}</pre>
        </div>
      )}

      {error && (
        <div className="bg-red-100 p-4 rounded shadow text-red-500">
          <h3 className="text-lg font-bold">Error:</h3>
          <pre>{error}</pre>
        </div>
      )}
    </div>
  );
};

export default Results;
