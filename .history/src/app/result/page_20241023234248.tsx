// Results.tsx
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
            <button onClick={handleRunScript}>Run Script</button>
            {response && <div>Response: {JSON.stringify(response)}</div>}
            {error && <div>Error: {error}</div>}
            <h1>{response}</h1>
        </div>
    </div>
  );
};

export default Results;
