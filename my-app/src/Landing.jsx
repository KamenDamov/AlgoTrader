import { useHistory } from 'react-router-dom';

const LandingPage = () => {
  const history = useHistory();

  const handleLoginClick = () => {
    history.push('/login');
  };

  const handleSignUpClick = () => {
    history.push('/signup');
  };

  return (
    <div>
      <h1></h1>
      <button onClick={handleLoginClick}>Log in</button>
      <button onClick={handleSignUpClick}>Sign up</button>
    </div>
  );
};
