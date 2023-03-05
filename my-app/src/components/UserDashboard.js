import React, { useEffect, useState } from 'react';
import axios from 'axios';

function UserDashboard() {
  const [userData, setUserData] = useState(null);
  const [newFunds, setNewFunds] = useState(0);
  

  useEffect(() => {
    const token = localStorage.getItem('token'); // Retrieve JWT from local storage

    // Set JWT in the Authorization header of the axios request
    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };

    // Query user data from the server using axios with the Authorization header
    axios.get('http://localhost:3001/getUserData', config)
      .then((response) => {
        setUserData(response.data);
      })
      .catch((error) => {
        console.log("merde")
        console.log(error);
      });
  }, []);

  const handleFundsChange = (event) => {
    setNewFunds(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const token = localStorage.getItem('token'); // Retrieve JWT from local storage

    // Set JWT in the Authorization header of the axios request
    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };

    // Modify the user's funds attribute in the database using axios with the Authorization header
    axios.post('http://localhost:3001/modifyFunds', { funds: newFunds }, config)
      .then((response) => {
        setUserData(response.data);
        setNewFunds(0);
      })
      .catch((error) => {
        console.log(error);
      });
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
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
    </div>
  );
}

export default UserDashboard;