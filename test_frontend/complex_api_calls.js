// Complex API call patterns for testing

import React from 'react';
import axios from 'axios';

// Custom API client with base URL
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
});

const ComplexApiExamples = () => {
  // Template literals with expressions
  const fetchUserDetails = async (userId) => {
    const response = await fetch(`/api/users/${userId}/details`);
    return response.json();
  };

  // Multiple fetch calls in one function
  const fetchUserWithPosts = async (userId) => {
    const [userResponse, postsResponse] = await Promise.all([
      fetch(`/api/users/${userId}`),
      fetch(`/api/users/${userId}/posts`)
    ]);
    
    const user = await userResponse.json();
    const posts = await postsResponse.json();
    
    return { user, posts };
  };

  // Nested API paths
  const fetchTeamMembers = async (orgId, teamId) => {
    return axios.get(`/api/organizations/${orgId}/teams/${teamId}/members`);
  };

  // API call with query parameters
  const searchProducts = async (query, category, page = 1) => {
    const response = await fetch(`/api/products/search?q=${query}&category=${category}&page=${page}`);
    return response.json();
  };

  // Using the custom API client
  const createOrder = async (orderData) => {
    return apiClient.post('/orders', orderData);
  };

  // Conditional API paths
  const fetchResource = async (resourceType, id) => {
    let endpoint;
    
    if (resourceType === 'user') {
      endpoint = `/api/users/${id}`;
    } else if (resourceType === 'product') {
      endpoint = `/api/products/${id}`;
    } else {
      endpoint = `/api/resources/${resourceType}/${id}`;
    }
    
    const response = await fetch(endpoint);
    return response.json();
  };

  // API call with dynamic segments and query parameters
  const fetchFilteredOrders = async (userId, filters) => {
    const { status, startDate, endDate, sort } = filters;
    const queryParams = new URLSearchParams();
    
    if (status) queryParams.append('status', status);
    if (startDate) queryParams.append('startDate', startDate);
    if (endDate) queryParams.append('endDate', endDate);
    if (sort) queryParams.append('sort', sort);
    
    const queryString = queryParams.toString();
    const endpoint = `/api/users/${userId}/orders${queryString ? `?${queryString}` : ''}`;
    
    return axios.get(endpoint);
  };

  // API call with request body from variable
  const updateUserPreferences = async (userId, preferences) => {
    const requestOptions = {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(preferences)
    };
    
    const response = await fetch(`/api/users/${userId}/preferences`, requestOptions);
    return response.json();
  };

  // Multiple axios method calls
  const userAPI = {
    getAll: () => axios.get('/api/users'),
    getById: (id) => axios.get(`/api/users/${id}`),
    create: (data) => axios.post('/api/users', data),
    update: (id, data) => axios.put(`/api/users/${id}`, data),
    delete: (id) => axios.delete(`/api/users/${id}`),
    updatePartial: (id, data) => axios.patch(`/api/users/${id}`, data)
  };

  // Non-standard API paths that should still be detected
  const authAPI = {
    login: (credentials) => fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    }),
    register: (userData) => axios.post('/auth/register', userData),
    verifyEmail: (token) => fetch(`/auth/verify-email?token=${token}`)
  };

  return (
    <div>
      {/* Component UI */}
    </div>
  );
};

export default ComplexApiExamples;