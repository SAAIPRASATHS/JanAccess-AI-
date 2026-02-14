import React, { useState, createContext } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';

// Low Bandwidth Context — toggles text-only mode app-wide
export const LowBandwidthContext = createContext({
  isLowBandwidth: false,
  toggleLowBandwidth: () => { },
});

// Persona Context — tracks the selected user persona app-wide
export const PersonaContext = createContext({
  persona: null,
  setPersona: () => { },
});

function App() {
  const [isLowBandwidth, setIsLowBandwidth] = useState(false);
  const [persona, setPersona] = useState(null);

  const toggleLowBandwidth = () => setIsLowBandwidth(prev => !prev);

  return (
    <PersonaContext.Provider value={{ persona, setPersona }}>
      <LowBandwidthContext.Provider value={{ isLowBandwidth, toggleLowBandwidth }}>
        <div className="App min-h-screen">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </LowBandwidthContext.Provider>
    </PersonaContext.Provider>
  );
}

export default App;
