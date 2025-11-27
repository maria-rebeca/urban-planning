import React from 'react';
import { Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar.jsx';
import Home from './pages/Home.jsx';
import Simulator from './pages/Simulator.jsx';
import Projects from './pages/Projects.jsx';
import Tutorial from './pages/Tutorial.jsx';

// --- ADAUGĂ LINIA ASTA ---
import ProposeProject from './pages/ProposeProject.jsx';

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/simulator" element={<Simulator />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/tutorial" element={<Tutorial />} />
        
        {/* Acum React știe ce este "ProposeProject" */}
        <Route path="/propose" element={<ProposeProject />} /> 
      </Routes>
    </div>
  );
}

export default App;