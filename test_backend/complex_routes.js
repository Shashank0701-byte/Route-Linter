// Complex Express.js route patterns for testing

const express = require('express');
const app = express();
const apiRouter = express.Router();
const authRouter = express.Router();

// Different route definition styles
app.get('/simple/route', (req, res) => {});

// With spaces and different quote styles
app.post(  "/spaced/route"  , (req, res) => {});
apiRouter.put(  '/api/items/:id'  , (req, res) => {});

// With middleware
apiRouter.delete('/api/items/:id', authenticate, (req, res) => {});

// Nested routes
authRouter.get('/auth/login', (req, res) => {});
authRouter.post('/auth/register', (req, res) => {});

// Route with query parameters (these don't affect the route pattern)
app.get('/search', (req, res) => {
  // Access query params with req.query.term
});

// Route with multiple path segments and parameters
app.get('/organizations/:orgId/teams/:teamId/members', (req, res) => {});

// Route with optional parameters (Express syntax)
app.get('/files/:filename?', (req, res) => {});

// Route with pattern matching parameters
app.get('/users/:userId(\\d+)', (req, res) => {});

// Route with wildcard
app.get('/assets/*', (req, res) => {});

module.exports = { app, apiRouter, authRouter };