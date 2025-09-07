#!/usr/bin/env python3

import argparse
import sys

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Route-Linter: A tool to analyze source code directories"
    )
    
    # Add required arguments
    parser.add_argument(
        "--backend", 
        required=True,
        help="Path to the backend directory"
    )
    parser.add_argument(
        "--frontend", 
        required=True,
        help="Path to the frontend directory"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Print the paths received
    print(f"Backend path: {args.backend}")
    print(f"Frontend path: {args.frontend}")
    
    # Exit successfully
    return 0

if __name__ == "__main__":
    sys.exit(main())