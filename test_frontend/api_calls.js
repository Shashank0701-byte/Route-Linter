// Sample React component with various API call patterns

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ApiExampleComponent = () => {
  const [users, setUsers] = useState([]);
  const [products, setProducts] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // Example using fetch with default GET method
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('/api/users');
        const data = await response.json();
        setUsers(data);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };
    
    fetchUsers();
  }, []);
  
  // Example using axios.get
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get('/api/products');
        setProducts(response.data);
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    };
    
    fetchProducts();
  }, []);
  
  // Example using fetch with explicit POST method
  const createUser = async (userData) => {
    setLoading(true);
    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });
      const newUser = await response.json();
      setUsers([...users, newUser]);
    } catch (error) {
      console.error('Error creating user:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Example using axios.post
  const createProduct = async (productData) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/products', productData);
      setProducts([...products, response.data]);
    } catch (error) {
      console.error('Error creating product:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Example using fetch with PUT method
  const updateUser = async (userId, userData) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/users/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });
      const updatedUser = await response.json();
      setUsers(users.map(user => user.id === userId ? updatedUser : user));
    } catch (error) {
      console.error('Error updating user:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Example using axios.put
  const updateProduct = async (productId, productData) => {
    setLoading(true);
    try {
      const response = await axios.put(`/api/products/${productId}`, productData);
      setProducts(products.map(product => product.id === productId ? response.data : product));
    } catch (error) {
      console.error('Error updating product:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Example using fetch with DELETE method
  const deleteUser = async (userId) => {
    setLoading(true);
    try {
      await fetch(`/api/users/${userId}`, {
        method: 'DELETE'
      });
      setUsers(users.filter(user => user.id !== userId));
    } catch (error) {
      console.error('Error deleting user:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Example using axios.delete
  const deleteProduct = async (productId) => {
    setLoading(true);
    try {
      await axios.delete(`/api/products/${productId}`);
      setProducts(products.filter(product => product.id !== productId));
    } catch (error) {
      console.error('Error deleting product:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Example using axios.patch
  const updateProductPartial = async (productId, partialData) => {
    setLoading(true);
    try {
      const response = await axios.patch(`/api/products/${productId}`, partialData);
      setProducts(products.map(product => product.id === productId ? response.data : product));
    } catch (error) {
      console.error('Error updating product:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Example with a non-API fetch call (should be ignored by the parser)
  const fetchExternalData = async () => {
    try {
      const response = await fetch('https://external-api.com/data');
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error('Error fetching external data:', error);
    }
  };
  
  // Example with a non-standard API path
  const fetchAuthStatus = async () => {
    try {
      const response = await fetch('/auth/status');
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error('Error fetching auth status:', error);
    }
  };
  
  return (
    <div>
      {/* Component UI */}
    </div>
  );
};

export default ApiExampleComponent;