import React, { useState } from "react";

function RegistrationPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Name:", name);
    console.log("Email:", email);
    // Here you can make an API call to register the user
  };

  return (
    <form onSubmit={handleSubmit}>
      <p>Sign up and test your AI and algorithmic trading strategy today</p>
      <label>
        Profile Name:
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </label>
      <br />
      <label>
        Email Address:
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </label>
      <br />
      <button type="submit">Register</button>
    </form>
  );
}

export default RegistrationPage;