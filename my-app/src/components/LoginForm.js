import {Link, useNavigate} from 'react-router-dom'
import React, { useState } from "react";
import axios from 'axios';
import "./style/login.css";
import './style/global.css';


function LoginForm() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!name || !password) {
      setError("Please enter your username and password");
      return;
    }

    const user = { name, password };

    axios.post("http://localhost:3001/login", user)
      .then((response) => {
        localStorage.setItem('token', response.data.token);
        console.log("Client side token: ", response.data);
        console.log("Logged in");
        navigate('/UserDashboard');
        // Store the access token in frontend state or in a cookie/local storage
      })
      .catch((error) => {
        console.error(error);
        setError("Unable to log in. Please try again.");
      });
  };

  return (
    <div className="hero-image">
      <div className="form-container">
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <label htmlFor="name">Username</label>
          <input
            type="text"
            id="name"
            name="name"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />

          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />

          <button type="login">Log in</button>
        </form>
        <Link to="/" className="back-to-landing-page">Back to landing page</Link>
      </div>
    </div>
  );
}

export default LoginForm;