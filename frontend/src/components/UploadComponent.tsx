'use client';

import React, { useRef, useState, ChangeEvent, useEffect } from 'react';
import { FiUpload, FiVideo } from 'react-icons/fi';
import Link from 'next/link';
import Image from 'next/image';
import axios from 'axios';
import { useSearchParams, useRouter } from 'next/navigation';

const UploadComponent = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const searchParams = useSearchParams();
  const router = useRouter();
  const didOpenRef = useRef(false);
  
  //sample videos data
  const sampleVideos = [
    { id: 1, image: '/images/test_pic1.png', videoId: 'sample1' },
    { id: 2, image: '/images/test_pic2.png', videoId: 'sample2' },
    { id: 3, image: '/images/test_pic3.png', videoId: 'sample3' },
    { id: 4, image: '/images/test_pic4.png', videoId: 'sample4' },
  ];

  //handle auto-open once, then clear the URL parameter
  useEffect(() => {
    const autoOpen = searchParams.get('autoOpen');
    
    //only run this once per component mount
    if (autoOpen === 'true' && !didOpenRef.current && fileInputRef.current) {
      //set the ref immediately to prevent multiple opens
      didOpenRef.current = true;
      
      //small delay to ensure component is fully mounted
      setTimeout(() => {
        fileInputRef.current?.click();
        
        //replace URL without the query parameter to prevent reopening on refresh
        const url = new URL(window.location.href);
        url.searchParams.delete('autoOpen');
        window.history.replaceState({}, '', url.toString());
      }, 100);
    }
  }, [searchParams]);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.includes('video/')) {
        alert('Please select a video file!');
        return;
      }
      setSelectedFile(file);
      console.log("Selected file:", file);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (!file.type.includes('video/')) {
        alert('Please drop a video file!');
        return;
      }
      setSelectedFile(file);
      console.log("Dropped file:", file);
    }
  };
  
  const handleUploadSubmit = async () => {
    if (!selectedFile) {
      alert('Please select a video file first!');
      return;
    }

    try {
      setIsUploading(true);
      setUploadProgress(0);
      
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await axios.post("http://localhost:8000/analyze", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setUploadProgress(percentCompleted);
          }
        }
      });
      
      if (response.data && response.data.processed_url) {
        router.push(`/analysis?videoUrl=${response.data.processed_url}&originalUrl=${response.data.original_url}`);
      } else {
        alert("Error processing video. Please try again.");
      }
    } catch (error) {
      console.error("Upload error:", error);
      alert("Error uploading video. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleSampleVideoClick = (videoId: string) => {
    //in a real app this would redirect to a pre-processed analysis
    router.push(`/analysis?sampleVideo=${videoId}`);
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="bg-black text-white min-h-screen">
      <div className="w-full max-w-xl mx-auto px-6 py-12">
        {/* Upload area */}
        <div className="space-y-4">
          <div 
            className={`p-10 rounded-3xl transition-colors w-full mx-auto min-h-[400px] border ${isDragging ? 'border-2 border-green-500' : 'border border-gray-700'}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <div className="flex flex-col items-center justify-center h-full text-center">
              {/* Plus icon */}
              <div className="flex justify-center mb-6">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="#22c55e" // Green-500 color
                  className="w-12 h-12"
                >
                  <path
                    fillRule="evenodd"
                    d="M12 3.75a.75.75 0 01.75.75v6.75h6.75a.75.75 0 010 1.5h-6.75v6.75a.75.75 0 01-1.5 0v-6.75H4.5a.75.75 0 010-1.5h6.75V4.5a.75.75 0 01.75-.75z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              
              {/*heading */}
              <h1 className="text-4xl font-bold text-white mb-8">
                Upload a video to<br />analyze your tennis shots
              </h1>
              
              {/*upload button */}
              <button 
                className="cursor-pointer bg-green-600 text-white text-3xl font-semibold py-4 px-10 rounded-full mb-6 hover:bg-green-500 transition-colors"
                onClick={handleUploadClick}
              >
                Upload Video
              </button>
              
              <input 
                ref={fileInputRef}
                id="file-upload" 
                type="file" 
                accept="video/*" 
                className="hidden"
                onChange={handleFileChange}
              />
              
              {/* Alternative text */}
              <p className="text-white text-2xl mb-1 font-semibold">
                or drop a file,
              </p>
              
              {/* URL option */}
              <p className="text-white mb-6">
                paste video or <span className="text-green-400 underline cursor-pointer">URL</span>
              </p>
              
              {/* Display selected file */}
              {selectedFile && (
                <div className="mt-4 p-4 bg-gray-800 rounded-lg w-full">
                  <div className="flex items-center">
                    <div className="bg-green-500 p-2 rounded mr-3">
                      <FiVideo className="text-black" size={20} />
                    </div>
                    <div className="text-left">
                      <p className="text-sm font-semibold truncate">{selectedFile.name}</p>
                      <p className="text-xs text-gray-400">
                        {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  
                  {isUploading && (
                    <div className="mt-3">
                      <div className="w-full bg-gray-700 rounded-full h-2.5">
                        <div 
                          className="bg-green-500 h-2.5 rounded-full" 
                          style={{ width: `${uploadProgress}%` }}
                        ></div>
                      </div>
                      <p className="text-xs text-gray-400 mt-1">
                        {uploadProgress < 100 ? 'Uploading...' : 'Processing...'}
                      </p>
                    </div>
                  )}
                  
                  {/* Analyze button */}
                  <button
                    onClick={handleUploadSubmit}
                    disabled={!selectedFile || isUploading}
                    className="mt-4 w-full bg-green-600 text-white text-lg font-semibold py-2 px-4 rounded-full hover:bg-green-500 transition-colors disabled:opacity-50"
                  >
                    {isUploading ? (
                      <>
                        <span className="mr-2">Processing...</span>
                        <span className="inline-block animate-spin h-4 w-4 border-2 border-white rounded-full border-t-transparent"></span>
                      </>
                    ) : (
                      "Analyze Video"
                    )}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Sample videos section */}
          <div className="max-w-sm mx-auto mt-6">
            <p className="text-gray-300 text-lg font-semibold text-center mb-4">
              No videos? Try one of these:
            </p>
            <div className="grid grid-cols-4 gap-4">
              {sampleVideos.map(video => (
                <div 
                  key={video.id}
                  className="cursor-pointer hover:opacity-80 transition-opacity"
                  onClick={() => handleSampleVideoClick(video.videoId)}
                >
                  <Image 
                    src={video.image} 
                    alt="Sample tennis shot" 
                    width={100} 
                    height={100} 
                    className="rounded-xl object-cover w-20 h-20"
                  />
                </div>
              ))}
            </div>
          
            {/* Terms of service */}
            <div className="mt-6 text-xs text-gray-500 text-center">
              By uploading a video or URL you agree to our{' '}
              <Link href="/terms" className="text-green-400 underline">Terms of Service</Link>.
              To learn more about how RacketVision handles your personal data, check our{' '}
              <Link href="/privacy" className="text-green-400 underline">Privacy Policy</Link>.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadComponent;