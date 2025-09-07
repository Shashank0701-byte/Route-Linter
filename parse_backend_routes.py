#!/usr/bin/env python3

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

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python parse_backend_routes.py <backend_directory>")
        sys.exit(1)
    
    backend_dir = sys.argv[1]
    routes = parse_backend_routes(backend_dir)
    
    print(f"Found {len(routes)} unique API routes:")
    for route in sorted(routes):
        print(f"  {route}")