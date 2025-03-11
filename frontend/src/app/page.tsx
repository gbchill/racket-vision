"use client";

import { ChangeEvent, useState } from "react";

export default function Home() {

  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  function handleFileSelect(e: ChangeEvent<HTMLInputElement>): void {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      // You can add more logic here to handle the selected file
      console.log("Selected file:", file);
    }
  }

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1 className="text-4xl font-bold text-center">Welcome to Racket Vision</h1>
      <div className="bg-gray-700 flex flex-col pl-50 pr-50 pt-45 pb-45  items-center rounded-4xl justify-center ">
      <input
        id="file-upload"
        type="file"
        accept="video/*"
        onChange={handleFileSelect}
        className="hidden"  // Hides the default input element
      />
      
      {/* Label styled as a button */}
      <label
        htmlFor="file-upload"
        className="cursor-pointer rounded bg-blue-600 text-3xl px-10 py-4 rounded-4xl text-white hover:bg-blue-700"
      >
        Upload Video
      </label>
      <p className="mt-4 text-center">
        {selectedFile ? (
          <span>
            Selected file: <strong>{selectedFile.name}</strong>
          </span>
        ) : (
          "No file selected"
        )}
      </p>
      </div>
    </div>
  );
}
