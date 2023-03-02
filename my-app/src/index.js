import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './components/style/signup.css';
import './components/style/login.css';
import Landing from './components/Landing';
import Login from './components/Login';
import SignUp from './components/SignUp';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Landing />} />
        <Route path="/Login" element={<Login/>} />
        <Route path="/SignUp" element={<SignUp/>} />
      </Routes>
    </Router>
  );
}

export default App;