#!/usr/bin/env python3

import argparse
import sys
import os
import re

def parse_backend_routes(directory):
    """
    Parse Express.js backend routes from JavaScript files in the given directory.
    
    Args:
        directory (str): Path to the backend directory
        
    Returns:
        set: A set of unique route strings in the format 'METHOD /path/to/route'
    """
    routes = set()
    
    # Regex pattern to match Express.js route definitions
    # This pattern matches common Express route patterns like:
    # app.get('/path', ...), router.post('/api/users', ...), etc.
    # Captures the HTTP method and the route path
    route_pattern = re.compile(
        r'(?:app|router|\w+Router)\.(get|post|put|delete|patch)\s*\(\s*[\'"](.*?)[\'"](\s*,|\))',
        re.IGNORECASE
    )
    
    # Walk through all files in the directory recursively
    for root, _, files in os.walk(directory):
        for file in files:
            # Only process JavaScript files
            if file.endswith('.js'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Find all route definitions in the file
                        for match in route_pattern.finditer(content):
                            method = match.group(1).upper()  # HTTP method (GET, POST, etc.)
                            path = match.group(2)           # Route path (/api/users, etc.)
                            
                            # Add the route to the set in the format 'METHOD /path'
                            routes.add(f'{method} {path}')
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    
    # Filter out any potential duplicates that might have different formatting
    # This is a safeguard in case the regex captures the same route multiple times
    unique_routes = set()
    for route in routes:
        # Normalize the route by removing extra spaces and standardizing format
        parts = route.split(' ', 1)
        if len(parts) == 2:
            method, path = parts
            unique_routes.add(f"{method} {path}")
    
    return unique_routes

def parse_frontend_calls(directory):
    """
    Parse API calls from JavaScript/React files in the given directory.
    
    Args:
        directory (str): Path to the frontend directory
        
    Returns:
        list: A list of dictionaries, each containing the HTTP method, route path, and file path
              where the API call was found
    """
    api_calls = []
    # Track unique calls to avoid duplicates
    unique_calls = set()
    
    # Regex patterns to match different API call patterns
    
    # Pattern for fetch API calls
    # Examples: fetch('/api/users'), fetch("/api/products"), fetch(`/api/items/${id}`)
    fetch_pattern = re.compile(
        r'fetch\s*\(\s*[\'"\`]([^\'"\`]+)[\'"\`]',
        re.IGNORECASE
    )
    
    # Pattern for fetch with method specification
    # Example: fetch('/api/users', { method: 'POST' })
    fetch_method_pattern = re.compile(
        r'fetch\s*\(\s*[\'"\`]([^\'"\`]+)[\'"\`]\s*,\s*\{[^\}]*method\s*:\s*[\'"](\w+)[\'"]',
        re.IGNORECASE
    )
    
    # Pattern for axios method calls
    # Examples: axios.get('/api/users'), axios.post('/api/products')
    axios_pattern = re.compile(
        r'axios\.(get|post|put|delete|patch)\s*\(\s*[\'"\`]([^\'"\`]+)[\'"\`]',
        re.IGNORECASE
    )
    
    # Walk through all files in the directory recursively
    for root, _, files in os.walk(directory):
        for file in files:
            # Only process JavaScript/JSX/TypeScript files
            if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Find all fetch API calls with explicit method
                        for match in fetch_method_pattern.finditer(content):
                            path = match.group(1)
                            method = match.group(2).upper()
                            
                            # Only include API calls (typically starting with /api)
                            if is_api_path(path):
                                # Create a unique key to avoid duplicates
                                unique_key = f"{method}:{path}:{file_path}"
                                if unique_key not in unique_calls:
                                    unique_calls.add(unique_key)
                                    api_calls.append({
                                        'method': method,
                                        'path': path,
                                        'file': file_path
                                    })
                        
                        # Find all fetch API calls (default method is GET)
                        for match in fetch_pattern.finditer(content):
                            path = match.group(1)
                            
                            # Only include API calls (typically starting with /api)
                            if is_api_path(path):
                                # Create a unique key to avoid duplicates
                                unique_key = f"GET:{path}:{file_path}"
                                # Check if this path was already found with an explicit method
                                if unique_key not in unique_calls:
                                    unique_calls.add(unique_key)
                                    api_calls.append({
                                        'method': 'GET',  # Default method for fetch is GET
                                        'path': path,
                                        'file': file_path
                                    })
                        
                        # Find all axios method calls
                        for match in axios_pattern.finditer(content):
                            method = match.group(1).upper()
                            path = match.group(2)
                            
                            # Only include API calls (typically starting with /api)
                            if is_api_path(path):
                                # Create a unique key to avoid duplicates
                                unique_key = f"{method}:{path}:{file_path}"
                                if unique_key not in unique_calls:
                                    unique_calls.add(unique_key)
                                    api_calls.append({
                                        'method': method,
                                        'path': path,
                                        'file': file_path
                                    })
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    
    return api_calls

def is_api_path(path):
    """
    Check if a path is likely an API endpoint.
    
    Args:
        path (str): The path to check
        
    Returns:
        bool: True if the path is likely an API endpoint, False otherwise
    """
    # Remove template literals (${var}) for the check
    clean_path = re.sub(r'\${[^}]*}', '', path)
    
    # Common API path patterns
    api_patterns = [
        # Standard API paths
        r'^/api',
        r'/api/',
        # Auth endpoints are often API calls
        r'^/auth',
        r'/auth/',
        # GraphQL endpoints
        r'^/graphql',
        # REST-like endpoints
        r'^/v\d+/',  # Version prefixes like /v1/, /v2/
    ]
    
    # Check if the path matches any of the API patterns
    for pattern in api_patterns:
        if re.search(pattern, clean_path):
            return True
    
    # Check if the path looks like a relative API path (no leading slash)
    if clean_path.startswith('api/') or clean_path.startswith('auth/'):
        return True
    
    # Exclude absolute URLs to external services
    if clean_path.startswith('http://') or clean_path.startswith('https://'):
        return False
    
    return False

def find_route_mismatches(backend_routes, frontend_calls):
    """
    Find mismatches between backend routes and frontend API calls.
    
    Args:
        backend_routes (set): Set of backend routes in the format 'METHOD /path'
        frontend_calls (list): List of dictionaries with frontend API calls
        
    Returns:
        tuple: (unused_routes, undefined_routes, suggestions)
            - unused_routes: Backend routes not used in the frontend
            - undefined_routes: Frontend API calls with no matching backend route
            - suggestions: Dictionary mapping undefined routes to suggested fixes
    """
    # Extract method and path from frontend calls
    frontend_routes = set()
    frontend_route_to_call = {}
    for call in frontend_calls:
        # Normalize the path by removing template literals
        path = re.sub(r'\${[^}]*}', ':param', call['path'])
        route_key = f"{call['method']} {path}"
        frontend_routes.add(route_key)
        frontend_route_to_call[route_key] = call
    
    # Find routes defined in backend but not used in frontend
    unused_routes = backend_routes - frontend_routes
    
    # Find routes used in frontend but not defined in backend
    undefined_routes = frontend_routes - backend_routes
    
    return unused_routes, undefined_routes, frontend_route_to_call

def main():
    parser = argparse.ArgumentParser(description='Route Linter - Analyze backend and frontend routes')
    parser.add_argument('--backend', required=True, help='Path to the backend directory')
    parser.add_argument('--frontend', required=True, help='Path to the frontend directory')
    parser.add_argument('--suggest', action='store_true', help='Suggest fixes for undefined routes using fuzzy matching')
    parser.add_argument('--threshold', type=int, default=70, help='Minimum similarity score for suggestions (0-100)')
    
    args = parser.parse_args()
    
    print(f"Backend path: {args.backend}")
    print(f"Frontend path: {args.frontend}")
    
    # Parse backend routes
    backend_routes = parse_backend_routes(args.backend)
    
    print(f"\nFound {len(backend_routes)} unique API routes in backend:")
    for route in sorted(backend_routes):
        print(f"  {route}")
    
    # Parse frontend API calls
    frontend_calls = parse_frontend_calls(args.frontend)
    
    print(f"\nFound {len(frontend_calls)} API calls in frontend:")
    for call in frontend_calls:
        print(f"  {call['method']} {call['path']} (in {os.path.relpath(call['file'], args.frontend)})")
    
    # Find mismatches between backend routes and frontend API calls
    unused_routes, undefined_routes, frontend_route_to_call = find_route_mismatches(backend_routes, frontend_calls)
    
    if unused_routes:
        print(f"\nWARNING: Found {len(unused_routes)} backend routes not used in frontend:")
        for route in sorted(unused_routes):
            print(f"  {route}")
    
    if undefined_routes:
        print(f"\nWARNING: Found {len(undefined_routes)} frontend API calls with no matching backend route:")
        
        # If suggestion is enabled, use fuzzy matching to find potential fixes
        if args.suggest:
            try:
                from thefuzz import process
                
                print("\nSuggested fixes (based on fuzzy matching):")
                for route in sorted(undefined_routes):
                    # Get the original call information
                    call = frontend_route_to_call[route]
                    file_path = os.path.relpath(call['file'], args.frontend)
                    
                    # Find the closest match from backend routes
                    closest_match, score = process.extractOne(route, backend_routes)
                    
                    # Only suggest if the score is above the threshold
                    if score >= args.threshold:
                        print(f"  In {file_path}:")
                        print(f"    {route} -> {closest_match} (similarity: {score}%)")
                    else:
                        print(f"  In {file_path}:")
                        print(f"    {route} -> No good match found (best: {closest_match}, similarity: {score}%)")
            except ImportError:
                print("\nNote: Install 'thefuzz' package for route suggestions: pip install thefuzz python-Levenshtein")
        else:
            # Just list the undefined routes without suggestions
            for route in sorted(undefined_routes):
                print(f"  {route}")
    
    if not unused_routes and not undefined_routes:
        print("\nSuccess! All backend routes are used in frontend and all frontend API calls have matching backend routes.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())