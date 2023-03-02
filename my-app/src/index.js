import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './signup.css';
import './login.css';
import Landing from './Landing';
import Login from './Login';
import SignUp from './SignUp';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="C:/Kamen/ML/AlgoTrader/my-app/src/Landing" component={Landing} />
        <Route path="/Login" component={Login} />
        <Route path="/SignUp" component={SignUp} />
      </Routes>
    </Router>
  );
}

export default App;