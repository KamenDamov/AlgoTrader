import { useState } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
const jwt = require('jsonwebtoken');
const { secret } = require('./config.js');

function LoginForm() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:3001/login', { name, password });
      const token = jwt.sign(response, secret, { expiresIn: '1h' });
      localStorage.setItem('token', token);      
      navigate('/UserDashboard');
    } catch (error) {
      console.error(error);
      alert('Invalid username or password');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Name:
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
      </label>
      <label>
        Password:
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </label>
      <button type="submit">Login</button>
    </form>
  );
}

export default LoginForm;
