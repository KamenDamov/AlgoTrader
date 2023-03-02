import { Link } from 'react-router-dom';
import React, { useState } from "react";
import "./style/signup.css";

function RegistrationForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("")
  const [funds, setFunds] = useState("")

  const handleSubmit = (event) => {
    event.preventDefault();
    
    const user = { name, email, password, funds };

    /*axios.post("/api/users", user)
      .then((response) => {
        console.log(response.data);
        // TODO: Add success message
      })
      .catch((error) => {
        console.error(error);
        // TODO: Add error message
      })*/
    };

  return (
    <div className="hero-image">
      <div className="form-container">
        <h2>
          Test your <span>AI and algorithmic trading strategy</span> today
        </h2>
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
          <Link to="/Landing">Back to landing page</Link>
        </form>
      </div>
    </div>
  );
}

export default RegistrationForm;
