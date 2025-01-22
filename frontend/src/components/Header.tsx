import React from 'react';

const Header = () => {
  return (
    <header className=" text-black p-4 shadow-sm ">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-4xl font-bold ml-5">Tennis Shot Analyzer</h1>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <a href="#about" className=" text-xl hover:underline">
                About
              </a>
            </li>
            <li>
              <a href="#info" className="text-xl hover:underline ml-5">
                How It Works
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
