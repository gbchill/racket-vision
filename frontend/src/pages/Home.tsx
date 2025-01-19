import React from 'react';
import Header from '../components/Header';
import HeroSection from '../components/HeroSection';
import FileUploader from '../components/FileUploader';
import Footer from '../components/Footer';

interface HomeProps {
  setProcessedVideoUrl: (url: string | null) => void;
}

const Home: React.FC<HomeProps> = ({ setProcessedVideoUrl }) => {
  return (
    <>
      <Header />
      <main className="">
        <HeroSection />
        <div className="py-10">
          <FileUploader setProcessedVideoUrl={setProcessedVideoUrl} />
        </div>
      </main>
      <Footer />
    </>
  );
};

export default Home;
