import { useState, useEffect } from 'react';
import axios from 'axios';

function UserData({ username }) {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    axios.get(`/api/users/${username}`)
      .then(response => {
        setUserData(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, [username]);

  if (!userData) {
    return <p>Loading user data...</p>;
  }

  return (
    <div>
      <h2>{userData.username}</h2>
      <p>Email: {userData.email}</p>
      <p>Funds: {userData.funds}</p>
    </div>
  );
}

export default UserData;