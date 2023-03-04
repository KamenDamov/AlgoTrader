import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './style/signup.css';
import './style/login.css';
import Landing from './Landing';
import Login from './LoginForm';
import SignUp from './SignUp';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Landing/>} />
        <Route path="/Login" element={<Login/>} />
        <Route path="/SignUp" element={<SignUp/>} />
      </Routes>
    </Router>
  );
}

export default App;
