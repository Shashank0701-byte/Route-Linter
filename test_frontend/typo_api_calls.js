// Test file with API calls that have typos or slight differences from backend routes

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UserComponent = () => {
  const [users, setUsers] = useState([]);
  const [products, setProducts] = useState([]);
  
  useEffect(() => {
    // Typo in 'users' (should be 'users')
    fetch('/api/usres')
      .then(response => response.json())
      .then(data => setUsers(data));
    
    // Typo in 'products' (should be 'products')
    axios.get('/api/productz')
      .then(response => setProducts(response.data));
    
    // Wrong HTTP method (should be POST)
    fetch('/api/users', {
      method: 'PUT',
      body: JSON.stringify({ name: 'John' }),
      headers: { 'Content-Type': 'application/json' }
    });
    
    // Extra segment in path (should be /api/products)
    axios.get('/api/products/all');
    
    // Missing segment in path (should be /api/users/:id)
    const userId = 123;
    fetch(`/api/users/${userId}/profile`);
    
    // Wrong HTTP method for existing route
    axios.delete('/api/products');
    
    // Completely wrong path
    fetch('/api/orders');
  }, []);
  
  return (
    <div>
      <h1>Users and Products</h1>
      {/* Component content */}
    </div>
  );
};

export default UserComponent;