import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserData() {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/user');
        setUserData(response.data);
      } catch (error) {
        console.log(error);
      }
    };

    fetchData();
  }, []);

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>User Data</h1>
      <ul>
        <li>Username: {userData.username}</li>
        <li>Email: {userData.Email}</li>
        <li>Password: {userData.password}</li>
        <li>Funds: {userData.funds}</li>
      </ul>
    </div>
  );
}

export default UserData;