import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './style/signup.css';
import './style/login.css';
import Landing from './Landing';
import Login from './LoginForm';
import SignUp from './SignUp';
import UserDashboard from './UserDashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Landing/>} />
        <Route path="/Login" element={<Login/>} />
        <Route path="/SignUp" element={<SignUp/>} />
        <Route path="/UserDashboard" element={<UserDashboard/>} />
      </Routes>
    </Router>
  );
}

export default App;
