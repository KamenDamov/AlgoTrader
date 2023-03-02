import React, { useState } from "react";
import "./login.css";

function RegistrationForm() {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("")

  const handleSubmit = (event) => {
    event.preventDefault();
    
    const user = { name, password };

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

          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
          
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default RegistrationForm;
