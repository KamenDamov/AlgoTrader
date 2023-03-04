import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './style/signup.css';
import './style/login.css';
import Landing from './Landing';
import Login from './LoginForm';
import SignUp from './SignUp';
import UserData from './UserData';

function App() {
  const isLoggedIn = true; // replace with your authentication logic

  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Landing />} />
        <Route path="/Login" element={<Login />} />
        <Route path="/SignUp" element={<SignUp />} />
        <PrivateRoute path="/UserData" element={<UserData />} isLoggedIn={isLoggedIn} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

function PrivateRoute({ element: Component, isLoggedIn, ...rest }) {
  return (
    <Route {...rest} element={isLoggedIn ? <Component /> : <Navigate to="/Login" />} />
  );
}

export default App;