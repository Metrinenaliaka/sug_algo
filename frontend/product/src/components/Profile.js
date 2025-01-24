import React, { useEffect, useState } from 'react';
import { getUserProfile } from '../services/api';
// import ProductCard from './ProductCard';

const Profile = () => {
  const [userProfile, setUserProfile] = useState(null);
  // const [recommendedProducts, setRecommendedProducts] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const data = await getUserProfile();
        setUserProfile(data);
      } catch (err) {
        setError('Failed to load user profile.');
      }
    };

    // const fetchRecommendations = async () => {
    //   try {
    //     const userId = localStorage.getItem('user_id');
    //     const products = await getProductRecommendations(userId);
    //     setRecommendedProducts(products);
    //   } catch (err) {
    //     setError('Failed to load recommendations.');
    //   }
    // };

    fetchUserProfile();
    // fetchRecommendations();
  }, []);

  return (
    <div>
      <h2>User Profile</h2>
      {userProfile ? (
        <div>
          <h3>Preferences</h3>
          <p>Preferred Product Type: {userProfile.preferred_product_type}</p>
          <p>Preferred Description: {userProfile.preferred_description}</p>

          <h3>Liked Products</h3>
          <ul>
            {userProfile.liked_products.map((product) => (
              <li key={product.id}>{product.name}</li>
            ))}
          </ul>

          <h3>Recommended Products</h3>
          {/* <div>
            {recommendedProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div> */}
        </div>
      ) : (
        <p>{error || 'Loading...'}</p>
      )}
    </div>
  );
};

export default Profile;