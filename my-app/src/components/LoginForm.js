import {Link, useNavigate} from 'react-router-dom'
import React, { useState } from "react";
import axios from 'axios';
import "./style/login.css";
import './style/global.css';


function LoginForm() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [password, setPassword] = useState("")

  const handleSubmit = (event) => {
    event.preventDefault();
    
    const user = { name, password };

    // Send login credentials to server and redirect to dashboard if successful
    /*axios.post('http://localhost:3001/login', { name, password }).then((response) => {
      if (response.data.success) {
        console.log("I wanna see my dashboard!")
        navigate('/UserDashboard');
      }
    }).catch((error) => {
      console.log(error);
    });*/

  axios.post("http://localhost:3001/login", user)
    .then((response) => {
      console.log(response.data);
      console.log("Logged in")
      navigate('/UserDashboard');
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