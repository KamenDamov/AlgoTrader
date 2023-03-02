import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Landing from './Landing';
import Login from './Login';
import SignUp from './SignUp';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="./Landing" component={Landing} />
        <Route path="./Login" component={Login} />
        <Route path="./SignUp" component={SignUp} />
      </Switch>
    </Router>
  );
}

export default App;
