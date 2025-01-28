import React, { useEffect, useState } from 'react';
import './Profile.css';
import { getUserProfile } from '../services/api';

const Profile = () => {
  const [userProfile, setUserProfile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const data = await getUserProfile();
        setUserProfile(data);
      } catch (err) {
        setError('Failed to load user profile.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="profile-container">
      <h2>User Profile</h2>
      {userProfile ? (
        <div>
          {/* Preferences Table */}
          <div className="profile-info">
            <h3>Preferences</h3>
            <table>
              <thead>
                <tr>
                  <th>Preference</th>
                  <th>Preferred Product Type</th>
                  <th>Preferred Description</th>
                </tr>
              </thead>
              <tbody>
                {userProfile.preferences && userProfile.preferences.length > 0 ? (
                  userProfile.preferences.map((preference, index) => (
                    <tr key={index}>
                      <td>Preference {index + 1}</td>
                      <td>{preference.preferred_product_type}</td>
                      <td>{preference.preferred_description}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="3" className="no-preferences">
                      No preferences available.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Interactions Table */}
          <div className="profile-info">
            <h3>Interactions</h3>
            <table>
              <thead>
                <tr>
                  <th>Product Name</th>
                  <th>Description</th>
                  <th>Interaction Type</th>
                  <th>Interaction Count</th>
                </tr>
              </thead>
              <tbody>
                {userProfile.interactions && userProfile.interactions.length > 0 ? (
                  userProfile.interactions.map((interaction, index) => (
                    <tr key={index}>
                      <td>{interaction.product_name}</td>
                      <td>{interaction.description}</td>
                      <td>{interaction.interaction_type}</td>
                      <td>{interaction.interaction_count}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="no-interactions">
                      No interactions available.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <p className="loading-error">{error || 'Failed to load profile'}</p>
      )}
    </div>
  );
};

export default Profile;
