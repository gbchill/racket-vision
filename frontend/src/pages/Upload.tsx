import React from "react";
import Header from '../components/Header';

interface UploadProps {
  videoUrl: string | null;
}

const Upload: React.FC<UploadProps> = ({ videoUrl }) => {
  if (!videoUrl) {
    return <p className="text-center mt-10">No video to display. Please try again.</p>;
  }

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = videoUrl;
    link.download = "processed-video.mp4";
    link.click();
  };

  return (
    <div className="bg-gray-300 min-h-screen">
         <Header />
      <div className=" bg-white shadow-lg p-8 rounded-2xl w-full flex flex-col items-center">
        <h2 className="text-2xl font-bold mb-6">Your Processed Video</h2>
        <video src={videoUrl} controls className="w-full max-w-lg rounded-lg shadow-lg mb-4"></video>
        <button
          onClick={handleDownload}
          className="mt-4 bg-blue-500 text-white py-2 px-6 rounded-lg hover:bg-blue-600"
        >
          Download Video
        </button>
      </div>
    </div>
  );
};

export default Upload;
