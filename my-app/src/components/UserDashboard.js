import React, { useEffect, useState } from 'react';
import axios from 'axios';

function UserDashboard() {
  const [userData, setUserData] = useState(null);
  const [newFunds, setNewFunds] = useState(0);

  useEffect(() => {
    
    // Query user data from the server using axios
    axios.get('http://localhost:3001/getUserData').then((response) => {
      setUserData(response.data);
    }).catch((error) => {
      console.log("merde")
      console.log(error);
    });
  }, []);

  const handleFundsChange = (event) => {
    setNewFunds(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Modify the user's funds attribute in the database using axios
    axios.post('http://localhost:3001/modifyFunds', { funds: newFunds }).then((response) => {
      setUserData(response.data);
      setNewFunds(0);
    }).catch((error) => {
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
