'use client';

import { ChangeEvent, useState } from 'react';
import { FiUpload } from 'react-icons/fi';
import Image from 'next/image';
import Link from 'next/link';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  function handleFileSelect(e: ChangeEvent<HTMLInputElement>): void {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      console.log("Selected file:", file);
    }
  }

  function handleDragOver(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(true);
  }

  function handleDragLeave(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(false);
  }

  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
      console.log("Dropped file:", e.dataTransfer.files[0]);
    }
  }

  return (
    <div className="bg-black text-white min-h-screen">
      <div className="max-w-7xl mx-auto px-6 py-16 flex flex-col lg:flex-row items-center">
        {/* Left side - Text content */}
        <div className="w-full lg:w-1/2 mb-12 lg:mb-0 lg:pr-12">
          <h1 className="text-5xl lg:text-6xl font-bold mb-6">
            Analyze Tennis <span className="text-green-500">Shots</span>
          </h1>
          <div className="flex mb-8">
            <h2 className="text-2xl font-bold">
              100% Automatically and <span className="bg-green-500 text-black px-3 py-1 rounded-md ml-1">Free</span>
            </h2>
          </div>
          <p className="text-lg text-gray-300 mb-8">
            Advanced AI technology instantly analyzes your tennis technique and provides actionable feedback to elevate your game.
          </p>
        </div>

        {/* Right side - Upload area and Sample Videos */}
        <div className="w-full lg:w-1/2 space-y-6">
          <div 
            className="bg-gray-900 p-15 rounded-3xl transition-colors w-full max-w-xl mx-auto h-110 shadow-[0_2px_8px_rgba(255,255,255,0.15)]"
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <div className="flex flex-col items-center justify-center h-full text-center pt-25">
                <label
                htmlFor="file-upload"
                className="cursor-pointer bg-green-600 text-white text-3xl font-semibold py-4 px-10 rounded-full mb-8 hover:bg-green-500 transition-colors"
                >
                Upload Video
                </label>
              
              <p className="text-white text-2xl mb-1 font-semibold">
                or drop a file,
              </p>
              <p className="text-white">
                paste image or <span className="text-green-400 underline">URL</span>
              </p>
              
              <input
                id="file-upload"
                type="file"
                accept="video/*"
                onChange={handleFileSelect}
                className="hidden"
              />
              
              {selectedFile && (
                <div className="mt-8 p-3 bg-gray-800 rounded-lg w-full">
                  <div className="flex items-center">
                    <div className="bg-green-500 p-2 rounded mr-3">
                      <FiUpload className="text-black" />
                    </div>
                    <div className="text-left">
                      <p className="text-sm font-semibold truncate">{selectedFile.name}</p>
                      <p className="text-xs text-gray-400">
                        {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Sample videos section moved below the upload area */}
          <div className="max-w-xl mx-auto mt-10">
            <div className="flex flex-col md:flex-row items-center gap-6">
              <div className="md:w-1/4 text-center">
                <p className="text-gray-300 text-lg font-semibold pr-13">
                  No video?
                </p>
                <p className="text-gray-300 text-lg font-semibold whitespace-nowrap" >
                Try one of these:
                </p>
              </div>
              <div className="md:w-3/4">
                <div className="grid grid-cols-4 gap-4">
                  <div className="cursor-pointer hover:opacity-80 transition-opacity">
                    <Image 
                      src="/images/test_pic1.png" 
                      alt="Sample tennis shot" 
                      width={100} 
                      height={100} 
                      className="rounded-2xl object-cover w-20 h-20"
                    />
                  </div>
                  <div className="cursor-pointer hover:opacity-80 transition-opacity">
                    <Image 
                      src="/images/test_pic2.png" 
                      alt="Sample tennis shot" 
                      width={100} 
                      height={100} 
                      className="rounded-2xl object-cover w-20 h-20"
                    />
                  </div>
                  <div className="cursor-pointer hover:opacity-80 transition-opacity">
                    <Image 
                      src="/images/test_pic3.png" 
                      alt="Sample tennis shot" 
                      width={100} 
                      height={100} 
                      className="rounded-2xl object-cover w-20 h-20"
                    />
                  </div>
                  <div className="cursor-pointer hover:opacity-80 transition-opacity">
                    <Image 
                      src="/images/test_pic4.png" 
                      alt="Sample tennis shot" 
                      width={100} 
                      height={100} 
                      className="rounded-2xl object-cover w-20 h-20"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-8 text-xs text-gray-500 ">
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
}
