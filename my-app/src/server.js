const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const bcrypt = require('bcrypt');
const { Pool } = require('pg');

// Create a new pool to manage database connections
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'financial_db',
  password: 'KaMendiNiO',
  port: 5432,
});

const app = express();

app.use(bodyParser.json());

// Add a middleware to parse JSON request bodies
app.use(express.json());

// Add CORS middleware
app.use(cors());

// Define a POST endpoint for creating new users
app.post('/api/users', (req, res) => {
  const { name, email, password, funds } = req.body;

  // Insert the new user into the database
  pool.query(
    'INSERT INTO users (username, email, password, funds) VALUES ($1, $2, $3, $4) RETURNING *',
    [name, email, password, funds],
    (err, result) => {
      if (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal server error' });
      } else {
        res.status(201).json({ message: 'User created successfully' });
      }
    }
  );
});

// Define a POST endpoint for user login
app.post('/login', (req, res) => {

  const { name, password } = req.body;

  // Check if the user exists in the database
  pool.query(
    'SELECT * FROM users WHERE username = $1 AND password = $2',
    [name, password],
    (err, result) => {
      if (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal server error' });
      } else if (result.rowCount === 0) {
        res.status(401).json({ error: 'Invalid username or password' });
      } else {
        res.status(200).json({ message: 'Login successful' });
      }
    }
  );
});

const authenticateUser = (req, res, next) => {
  console.log(req.body);
  const { name, password } = req.body;
  
  // Check the database to see if the user exists and the password is correct
  pool.query(
    'SELECT * FROM users WHERE username = $1 AND password = $2',
    [name, password],
    (err, result) => {
      if (err) {
        console.log("fuck")
        console.error(err);
        res.status(500).json({ error: 'Internal server error' });
      } else if (result.rowCount === 0) {
        res.status(401).json({ error: 'Invalid username or password' });
      } else {
        
        // Attach the user object to req.user
        req.user = result.rows[0];
        next();
      }
    }
  );
};

app.get('/getUserData', authenticateUser, (req, res) => {
  const { username, funds } = req.user;
  
  // Return user data
  res.status(200).json({ username, funds });
});

app.post('/modifyFunds', authenticateUser, (req, res) => {
  const { funds } = req.body;
  const { username } = req.user;

  // Update user funds in the database
  pool.query(
    'UPDATE users SET funds = funds + $1 WHERE username = $2 RETURNING username, funds',
    [funds, username],
    (err, result) => {
      if (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal server error' });
      } else if (result.rowCount === 0) {
        res.status(404).json({ error: 'User not found' });
      } else {
        res.status(200).json(result.rows[0]);
      }
    }
  );
});

// Start the server
app.listen(3001, () => {
  console.log('Server listening on port 3001');
});
