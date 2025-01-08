import React, { useState } from 'react';
import axios from 'axios';

import { FiPlus } from 'react-icons/fi'; // Importing a plus icon from react-icons

const FileUploader = () => {
  const [file, setFile] = useState<File | null>(null);

  // Handle file input change
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const [analysisResult, setAnalysisResult] = useState<string | null>(null);


  // Handle upload click
const handleUpload = async () => {
  if (!file) {
    alert('Please select a file to upload!');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('http://127.0.0.1:5000/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    setAnalysisResult(response.data.feedback.join('\n')); // Store the feedback
  } catch (error) {
    console.error('Error uploading video:', error);
    alert('Failed to analyze the video.');
  }
};

  

  return (
    <div className=" w-full max-w-5xl mx-auto mt-10">
      <div className="border-4 border-spacing-3 border-black shadow-lg bg-white p-8 rounded-2xl w-full h-[500px] flex flex-col items-center justify-center">
        {/* File Input */}
        <input
          type="file"
          accept="video/*"
          onChange={handleFileChange}
          className="hidden"
          id="file-input"
        />

        {/* Label with Plus Icon */}
        <label
          htmlFor="file-input"
          className="cursor-pointer flex flex-col items-center justify-center text-gray-500 hover:text-blue-500"
        >
          {/* Plus Icon */}
          <FiPlus size={60} className="mb-2 bg-slate-100 shadow-lg rounded-full" />
        </label>

        {/* Display Selected File Name */}
        {file && <p className="mt-4 text-gray-700">{file.name}</p>}

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          className="mt-6 bg-blue-500 text-white py-2 px-6 rounded-lg hover:bg-blue-600"
        >
          Analyze Video
        </button>
        {analysisResult && (
  <div className="mt-6 p-4 bg-gray-100 border border-gray-300 rounded">
    <h3 className="text-lg font-bold mb-2">Analysis Result:</h3>
    <pre className="whitespace-pre-wrap">{analysisResult}</pre>
  </div>
)}
      </div>
    </div>
  );
};

export default FileUploader;
