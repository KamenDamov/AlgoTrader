const express = require('express');
const { Pool } = require('pg');

// Create a new pool to manage database connections
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'financial_db',
  password: 'KaMendiNiO',
  port: 5432,
});

const router = express.Router();

router.post('/login', (req, res) => {
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

module.exports = router;
