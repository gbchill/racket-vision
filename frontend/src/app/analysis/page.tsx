'use client';

import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { FiDownload, FiShare2 } from 'react-icons/fi';
import Link from 'next/link';

const AnalysisPage = () => {
  const searchParams = useSearchParams();
  const processedVideoUrl = searchParams.get('videoUrl');
  const originalVideoUrl = searchParams.get('originalUrl');
  const sampleVideo = searchParams.get('sampleVideo');
  
  const [activeTab, setActiveTab] = useState<'processed' | 'original'>('processed');
  const [isDownloading, setIsDownloading] = useState(false);

  // For sample videos - in a real app, these would be loaded from a database
  const getSampleVideoData = (id: string) => {
    const samples: Record<string, { processedUrl: string, originalUrl: string, title: string }> = {
      'sample1': {
        processedUrl: '/samples/processed-forehand.mp4',
        originalUrl: '/samples/original-forehand.mp4',
        title: 'Professional Forehand Example'
      },
      // Add more sample videos as needed
    };
    
    return samples[id] || null;
  };

  // Determine which video URLs to use (real upload or sample)
  let currentProcessedUrl = processedVideoUrl;
  let currentOriginalUrl = originalVideoUrl;
  let analysisTitle = 'Your Tennis Swing Analysis';
  
  if (sampleVideo) {
    const sampleData = getSampleVideoData(sampleVideo);
    if (sampleData) {
      currentProcessedUrl = sampleData.processedUrl;
      currentOriginalUrl = sampleData.originalUrl;
      analysisTitle = sampleData.title;
    }
  }

  // Handle video download
  const handleDownload = async (url: string | null, type: string) => {
    if (!url) return;
    
    try {
      setIsDownloading(true);
      
      // Fetch the video
      const response = await fetch(url);
      const blob = await response.blob();
      
      // Create a download link
      const downloadLink = document.createElement('a');
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = `racketvision-${type}-${Date.now()}.mp4`;
      
      // Trigger download
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
      
    } catch (error) {
      console.error('Download error:', error);
      alert('Error downloading video');
    } finally {
      setIsDownloading(false);
    }
  };

  // Handle share
  const handleShare = () => {
    if (navigator.share && currentProcessedUrl) {
      navigator.share({
        title: 'My Tennis Analysis by RacketVision',
        text: 'Check out my tennis swing analysis!',
        url: window.location.href
      })
      .catch(error => console.error('Error sharing:', error));
    } else {
      // Fallback if Web Share API is not available
      navigator.clipboard.writeText(window.location.href)
        .then(() => alert('Link copied to clipboard!'))
        .catch(error => console.error('Error copying to clipboard:', error));
    }
  };

  if (!currentProcessedUrl && !sampleVideo) {
    return (
      <div className="bg-black text-white min-h-screen flex flex-col items-center justify-center p-6">
        <div className="text-center max-w-md">
          <h1 className="text-3xl font-bold mb-4">No Video Found</h1>
          <p className="mb-8">Please upload a video first to see your analysis.</p>
          <Link 
            href="/upload" 
            className="bg-green-600 text-white font-semibold py-3 px-6 rounded-full hover:bg-green-500 transition-colors"
          >
            Upload Video
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-black text-white min-h-screen">
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold mb-4">{analysisTitle}</h1>
        
        {/* Video player and controls */}
        <div className="bg-gray-900 rounded-2xl p-6 mb-8 shadow-lg">
          {/* Tabs */}
          <div className="flex border-b border-gray-700 mb-4">
            <button
              className={`px-4 py-2 ${activeTab === 'processed' ? 'text-green-500 border-b-2 border-green-500 font-medium' : 'text-gray-400'}`}
              onClick={() => setActiveTab('processed')}
            >
              Analyzed Video
            </button>
            <button
              className={`px-4 py-2 ${activeTab === 'original' ? 'text-green-500 border-b-2 border-green-500 font-medium' : 'text-gray-400'}`}
              onClick={() => setActiveTab('original')}
              disabled={!currentOriginalUrl}
            >
              Original Video
            </button>
          </div>
          
          {/* Video player */}
          <div className="relative aspect-video bg-black rounded-lg overflow-hidden">
            <video 
              key={activeTab} // Force reload when tab changes
              src={activeTab === 'processed' ? currentProcessedUrl || '' : currentOriginalUrl || ''}
              controls 
              className="w-full h-full"
              autoPlay
            />
          </div>
          
          {/* Actions */}
          <div className="flex justify-between mt-4">
            <div className="text-sm text-gray-400">
              {activeTab === 'processed' ? 'Video with MediaPipe pose tracking overlay' : 'Original uploaded video'}
            </div>
            <div className="flex space-x-3">
              <button
                onClick={() => handleDownload(
                  activeTab === 'processed' ? currentProcessedUrl : currentOriginalUrl,
                  activeTab
                )}
                disabled={isDownloading}
                className="flex items-center text-sm text-white bg-gray-800 hover:bg-gray-700 px-3 py-1 rounded-md transition-colors"
              >
                <FiDownload className="mr-2" />
                {isDownloading ? 'Downloading...' : 'Download'}
              </button>
              <button
                onClick={handleShare}
                className="flex items-center text-sm text-white bg-gray-800 hover:bg-gray-700 px-3 py-1 rounded-md transition-colors"
              >
                <FiShare2 className="mr-2" />
                Share
              </button>
            </div>
          </div>
        </div>
        
        {/* Analysis details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gray-900 rounded-xl p-6">
            <h2 className="text-xl font-bold mb-3">Pose Analysis</h2>
            <p className="text-gray-300 mb-4">
              Your video has been analyzed using MediaPipe's pose tracking technology. The colored 
              lines and landmarks show your body's key points throughout the swing.
            </p>
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="font-medium text-green-400 mb-2">Key Points:</h3>
              <ul className="list-disc list-inside text-gray-300 space-y-1">
                <li>Pay attention to your arm extension through the swing</li>
                <li>Watch your weight transfer from back to front foot</li>
                <li>Notice your shoulder rotation during follow-through</li>
                <li>Compare your form with professional players for best results</li>
              </ul>
            </div>
          </div>
          
          <div className="bg-gray-900 rounded-xl p-6">
            <h2 className="text-xl font-bold mb-3">Technical Information</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <h3 className="text-sm font-medium text-gray-400">Processing</h3>
                <p className="text-gray-300">MediaPipe Pose Detection</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-400">Model</h3>
                <p className="text-gray-300">BlazePose GHUM 3D</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-400">Points Tracked</h3>
                <p className="text-gray-300">33 Body Landmarks</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-400">Confidence</h3>
                <p className="text-gray-300">≥ 0.5 Threshold</p>
              </div>
            </div>
            
            <div className="mt-6">
              <h3 className="font-medium text-green-400 mb-2">Next Steps:</h3>
              <div className="flex flex-col space-y-3">
                <Link
                  href="/upload"
                  className="text-center bg-green-600 text-white font-medium py-2 px-4 rounded-lg hover:bg-green-500 transition-colors"
                >
                  Analyze Another Video
                </Link>
                <button
                  className="text-center bg-gray-800 text-white font-medium py-2 px-4 rounded-lg hover:bg-gray-700 transition-colors"
                >
                  Compare With Pro Analysis
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPage;