import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BusinessUpload from './pages/BusinessUpload';
import UserBrowse from './pages/UserBrowse';
import './App.css';

function Home() {
  return (
    <div className="home-container">
      <div className="card" onClick={() => window.location.href = '/user'}>
        <h2>User</h2>
        <p>Have a question?</p>
      </div>
      <div className="card" onClick={() => window.location.href = '/upload'}>
        <h2>Business</h2>
        <p>Upload your catalogue</p>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/user" element={<UserBrowse />} />
        <Route path="/upload" element={<BusinessUpload />} />
      </Routes>
    </Router>
  );
}

export default App;
