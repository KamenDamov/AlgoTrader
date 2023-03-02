import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import './components/style/signup.css';
import './components/style/login.css';
import Landing from './components/Landing';
import Login from './components/Login';
import SignUp from './components/SignUp';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Landing} />
        <Route path="/Login" component={Login} />
        <Route path="/SignUp" component={SignUp} />
      </Switch>
    </Router>
  );
}

export default App;