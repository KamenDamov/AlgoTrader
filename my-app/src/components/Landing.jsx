import { Link } from 'react-router-dom';

const Landing = () => {
  return (
    <div>
      <h2>
          Test your <span>AI and algorithmic trading strategy</span> today
      </h2>
      <Link to = '/Login'>Log in</Link>
      <Link to = '/SignUp'>Sign up</Link>
    </div>
  );
};

export default Landing;