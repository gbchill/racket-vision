import React from 'react';
import Header from '../components/Header';
import HeroSection from '../components/HeroSection';
import FileUploader from '../components/FileUploader';
import Footer from '../components/Footer';

const Home = () => {
  return (
    <>
      <Header />
      <main className="">
        <HeroSection />
        <div className="py-10">
          <FileUploader />
        </div>
      </main>
      <Footer />
    </>
  );
};

export default Home;
