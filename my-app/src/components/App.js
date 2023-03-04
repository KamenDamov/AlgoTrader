import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './style/signup.css';
import './style/login.css';
import Landing from './Landing';
import Login from './LoginForm';
import SignUp from './SignUp';
import UserData from './UserData';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Landing/>} />
        <Route path="/Login" element={<Login/>} />
        <Route path="/SignUp" element={<SignUp/>} />
        <Route path="/UserData" element={<UserData/>} />
      </Routes>
    </Router>
  );
}

export default App;
