import "./style/signup.css";
import axios from 'axios';
import React, { useState } from "react";
import {Link} from 'react-router-dom'

function RegistrationForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("")
  const [funds, setFunds] = useState("")

  const handleSubmit = async (event) => {
    event.preventDefault();

    const user = { name, email, password, funds };

    try {
      console.log(user)
      const response = await axios.post('http://localhost:3001/api/users', user);
      console.log(response.data);
      console.log("Works")
    } catch (error) {
      console.error(error);
      console.log("Doesnt work")
    }
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

          <label htmlFor="email">Email Address</label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />

          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
          <label htmlFor="funds">Add funds</label>
          <input
            type="number"
            min = '0'
            id="funds"
            name="funds"
            value={funds}
            onChange={(event) => setFunds(event.target.value)}
          />

          <button type="submit">Submit</button>
        </form>
        <Link to="/" className="back-to-landing-page">Back to landing page</Link>
      </div>
    </div>
  );
}

export default RegistrationForm;
