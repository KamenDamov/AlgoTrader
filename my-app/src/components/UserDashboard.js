import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function UserDashboard() {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [newFunds, setNewFunds] = useState(0);

  useEffect(() => {

    const token = localStorage.getItem('token');
    console.log(token)

    if (!token) {
      navigate('/login');
      return;
    }

    const config = {
      headers: {
        Authorization: `Bearer ${token.secret}`,
      },
    };
    
    console.log(config)
  //Code is good until here
    axios.get('http://localhost:3001/getUserData', config)
      .then((response) => {
        setUserData(response.data);
      })
      .catch((error) => {
        if (error.response.status === 401) {
          console.log("SOME ERROR");
          localStorage.removeItem('token');
          navigate('/login');
        } else {
          console.log(error);
        }
      });
  }, []);

  const handleFundsChange = (event) => {
    setNewFunds(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const token = localStorage.getItem('token');

    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };

    axios.post('http://localhost:3001/modifyFunds', { funds: newFunds }, config)
      .then((response) => {
        setUserData(response.data);
        setNewFunds(0);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div>
      {userData ? (
        <div>
          <h1>Welcome, {userData.username}!</h1>
          <p>Your current funds: ${userData.funds}</p>
          <form onSubmit={handleSubmit}>
            <label>
              Add Funds:
              <input type="number" value={newFunds} onChange={handleFundsChange} />
            </label>
            <button type="submit">Submit</button>
          </form>
          <button onClick={handleLogout}>Log Out</button>
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
    </div>
  );
}

export default UserDashboard;