'use client'

import React from 'react'
import { useSearchParams } from 'next/navigation'


const AnalysisPage = () => {
    const searchParams = useSearchParams();
    const videoUrl = searchParams.get('videoUrl');

    if(!videoUrl) {
      return <div className="text-center p-10">
          No video found. Please upload a video first.</div>;
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Your Tennis Swing Analysis</h1>
      
      <div className="bg-gray-800 rounded-lg p-6">
        <video 
          src={videoUrl} 
          controls 
          className="w-full max-w-3xl mx-auto rounded-lg mb-6"
        ></video>
        
        <div className="text-white">
          <h2 className="text-xl font-bold mb-3">Analysis Results</h2>
          <p>Your video has been processed with MediaPipe pose tracking.</p>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPage;
