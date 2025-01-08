import React from 'react';

const Header = () => {
  return (
    <header className=" text-black p-4 ">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold ml-5">Tennis Shot Analyzer</h1>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <a href="#about" className="hover:underline">
                About
              </a>
            </li>
            <li>
              <a href="#info" className="hover:underline">
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
