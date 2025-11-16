
import React from 'react';
import { Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar.jsx';
import Home from './pages/Home.jsx';
import Simulator from './pages/Simulator.jsx';
import Projects from './pages/Projects.jsx';
import Tutorial from './pages/Tutorial.jsx';

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/simulator" element={<Simulator />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/tutorial" element={<Tutorial />} />
      </Routes>
    </div>
  );
}

export default App;