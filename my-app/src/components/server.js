const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const bcrypt = require('bcrypt');
const { secret } = require('./config.js');
const { Pool } = require('pg');
const jwt = require('jsonwebtoken');

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'financial_db',
  password: 'KaMendiNiO',
  port: 5432,
});

const app = express();

app.use(bodyParser.json());

app.use(express.json());

app.use(cors({
  origin: 'http://localhost:3000', // replace with the URL of your React app
  credentials: true,
}));

app.post('/api/users', (req, res) => {
  const { name, email, password, funds } = req.body;

  bcrypt.hash(password, 10, (err, hash) => {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal server error' });
    } else {
      pool.query(
        'INSERT INTO users (username, email, password, funds) VALUES ($1, $2, $3, $4) RETURNING *',
        [name, email, hash, funds],
        (err, result) => {
          if (err) {
            console.error(err);
            res.status(500).json({ error: 'Internal server error' });
          } else {
            res.status(201).json({ message: 'User created successfully' });
          }
        }
      );
    }
  });
});

app.post('/login', (req, res) => {
  const { name, password } = req.body;
  console.log(name, password);
  pool.query(
    'SELECT * FROM users WHERE username = $1',
    [name],
    (err, result) => {
      console.log(result);
      if (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal server error' });
      } else if (result.rowCount === 0) {
        res.status(401).json({ error: 'Invalid username or password' });
      } else {
        const user = result.rows[0];

        bcrypt.compare(password, user.password, (err, isValid) => {
          if (err) {
            console.error(err);
            res.status(500).json({ error: 'Internal server error' });
          } else if (!isValid) {
            res.status(401).json({ error: 'Invalid username or password' });
          } else {
            const token = jwt.sign({ userId: user.id }, 'secret_key', { expiresIn: '1h' });
            res.status(200).json({ token });
          }
        });
      }
    }
  );
});

const authenticateUser = (req, res, next) => {
  const token = req.headers.authorization;

  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    console.log("REad token: ", token);
    const jwtToken = token.substring(7); // remove "Bearer " from the token
    console.log(jwtToken, secret);
    const decodedToken = jwt.verify(jwtToken, secret);
    console.log("Server side token: ", decodedToken);   // Add this line to check the decoded token
    const userId = decodedToken.userId;
    console.log(userId);

    pool.query(
      'SELECT * FROM users WHERE id = $1',
      [userId],
      (err, result) => {
        if (err) {
          console.error(err);
          res.status(500).json({ error: 'Internal server error' });
        } else if (result.rowCount === 0) {
          res.status(401).json({ error: 'Unauthorized' });
        } else {
          req.user = result.rows[0];
          next();
        }
      }
    );
  } catch (err) {
    console.log(err);
    res.status(401).json({ error: 'Unauthorized' });
  }
};

app.get('/getUserData', authenticateUser, (req, res) => {
  const {username, funds } = req.user;

  // Return user data
  res.status(200).json({ username, funds });
  });
  
  // Define a POST endpoint to modify the user's funds
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