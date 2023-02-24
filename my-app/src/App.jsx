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
      <p>Test your AI and algorithmic trading strategy today</p>
    </form>
  );
}

export default RegistrationPage;