import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './style/signup.css';
import './style/login.css';
import Landing from './Landing';
import Login from './LoginForm';
import SignUp from './SignUp';
import UserDashboard from './UserDashboard';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);

  const handleLogin = (data) => {
    setUserData(data);
    setLoggedIn(true);
  };

  const handleLogout = () => {
    setUserData(null);
    setLoggedIn(false);
  };

  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Landing />} />
        <Route path="/Login" element={<Login handleLogin={handleLogin} />} />
        <Route path="/SignUp" element={<SignUp />} />
        {loggedIn ? (
          <Route
            path="/UserDashboard"
            element={<UserDashboard userData={userData} handleLogout={handleLogout} />}
          />
        ) : null}
      </Routes>
    </Router>
  );
}

export default App;