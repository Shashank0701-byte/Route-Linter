#!/usr/bin/env python3

import os
import re

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
        # Exclude common non-API paths
        # r'^/static/',
        # r'^/assets/',
        # r'^/images/',
        # r'^/css/',
        # r'^/js/'
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

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python parse_frontend_calls.py <frontend_directory>")
        sys.exit(1)
    
    frontend_dir = sys.argv[1]
    api_calls = parse_frontend_calls(frontend_dir)
    
    print(f"Found {len(api_calls)} API calls:")
    for call in api_calls:
        print(f"  {call['method']} {call['path']} (in {call['file']})")