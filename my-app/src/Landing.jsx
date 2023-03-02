import { useHistory } from 'react-router-dom';

const Landing = () => {
  const history = useHistory();

  const handleLoginClick = () => {
    history.push('./Login');
  };

  const handleSignUpClick = () => {
    history.push('./SignUp');
  };

  return (
    <div>
      <h1></h1>
      <button onClick={handleLoginClick}>Log in</button>
      <button onClick={handleSignUpClick}>Sign up</button>
    </div>
  );
};
