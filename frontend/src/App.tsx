import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Upload from "./pages/Upload";

function App() {
  const [processedVideoUrl, setProcessedVideoUrl] = useState<string | null>(null);

  return (
    <div className="bg-gray-300 min-h-screen">
      <Routes>
        <Route
          path="/"
          element={<Home setProcessedVideoUrl={setProcessedVideoUrl} />}
        />
        <Route
          path="/upload"
          element={
            <Upload videoUrl={processedVideoUrl} />
          }
        />
      </Routes>
    </div>
  );
}

export default App;
