import React, { useState } from "react";
import "./index.css";

/*
import axios from "axios";

const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const bodyParser = require('body-parser');

// Create a new Express app
const app = express();
const port = 5000;

// Enable CORS
app.use(cors());

// Enable body parsing middleware
app.use(bodyParser.json());

// Create a new table in the database
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS users (
    Username TEXT NOT NULL,
    Email TEXT NOT NULL,
    Password TEXT NOT NULL,
    )
  `);
});

app.post('/api/users', (req, res) => {
  const { name, email, password } = req.body;

  // Insert a new user into the database
  db.run('INSERT INTO users (name, email) VALUES (?, ?, ?)', [name, email, password], (err) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'Failed to insert user into database' });
    }

    return res.status(200).json({ message: 'User created successfully' });
  });
});
  app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
  });

//Use to create a new user
class RegistrationService extends React.Component {
  updateUser(name, email) {
    return axios.put(`/api/users/${name}`, { name, email, password });
  }

  render() {
    return null;
  }
}

export default RegistrationService;*/

function RegistrationForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("")

  const handleSubmit = (event) => {
    event.preventDefault();
    
    const user = { name, email, password };

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
          <label htmlFor="name">Profile Name</label>
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

          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default RegistrationForm;
