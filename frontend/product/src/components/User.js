import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserProfile = ({ setUsername }) => {  // Accept setUsername as a prop
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/current_user/', {
          withCredentials: true,  // Make sure the session cookie is sent
        });
        setUsername(response.data.username);  // Set the username in the parent state
        setEmail(response.data.email);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching user data:', error);
        setLoading(false);
      }
    };

    fetchUserData();
  }, [setUsername]);  // Ensure setUsername is included in the dependency array

  return (
    <div>
      {loading ? (
        <p>Loading user info...</p>
      ) : (
        <div>
          <h2>Welcome, {setUsername}!</h2>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
