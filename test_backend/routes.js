// Sample Express.js routes for testing

const express = require('express');
const router = express.Router();

// User routes
router.get('/api/users', (req, res) => {
  // Get all users
});

router.post('/api/users', (req, res) => {
  // Create a new user
});

router.get('/api/users/:id', (req, res) => {
  // Get user by ID
});

router.put('/api/users/:id', (req, res) => {
  // Update user
});

router.delete('/api/users/:id', (req, res) => {
  // Delete user
});

// Product routes
app.get('/api/products', function(req, res) {
  // Get all products
});

app.post('/api/products', function(req, res) {
  // Create a product
});

app.patch('/api/products/:id', function(req, res) {
  // Update product partially
});

module.exports = router;