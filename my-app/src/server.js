const express = require('express');
const cors = require('cors');
const loginRouter = require('./loging');
const { Pool } = require('pg');

// Create a new pool to manage database connections
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'financial_db',
  password: 'KaMendiNiO',
  port: 5432,
});

// Create a new express application
const app = express();

// Parse JSON request bodies
app.use(express.json());

app.use('/api', loginRouter);

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
        console.log("ERROR WHEN INPUTING")
        res.status(500).json({ error: 'Internal server error' });
      } else {
        res.status(201).json({ message: 'User created successfully' });
        console.log("Properly input")
      }
    }
  );
});

// Start the server
app.listen(3000, () => {
  console.log('Server listening on port 3000');
});