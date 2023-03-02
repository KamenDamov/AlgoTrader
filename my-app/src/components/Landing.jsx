import React from 'react';
import { Link } from 'react-router-dom';
import './style/landing.css';

const Landing = () => {
  return (
    <div className="landing-container">
      <h2>
          Test your <span>AI and algorithmic trading strategy</span> today
      </h2>
      <Link to = '/Login' className='button'>Log in</Link>
      <Link to = '/SignUp' className='button'>Sign up</Link>
    </div>
  );
};

export default Landing;