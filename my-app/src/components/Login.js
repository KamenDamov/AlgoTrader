import {Link} from 'react-router-dom'
import React, { useState } from "react";
import axios from 'axios';
import "./style/login.css";
import './style/global.css';


function LoginForm() {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("")

  const handleSubmit = (event) => {
    event.preventDefault();
    
    const user = { name, password };

  axios.post("/api/login/", user)
    .then((response) => {
      console.log(response.data);
      console.log("Logged in")
      // Store the access token in frontend state or in a cookie/local storage
    })
    .catch((error) => {
      console.error(error);
      console.log("Can't log in")
    });
    };

  return (
    <div className="hero-image">
      <div className="form-container">
        
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
