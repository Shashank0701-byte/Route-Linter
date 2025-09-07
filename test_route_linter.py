#!/usr/bin/env python3

import unittest
import subprocess
import sys
import os

class TestRouteLinter(unittest.TestCase):
    
    def test_required_arguments(self):
        """Test that the script requires both arguments"""
        # Test missing both arguments
        result = subprocess.run(
            [sys.executable, "route_linter.py"],
            capture_output=True,
            text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required", result.stderr)
        
        # Test missing frontend argument
        result = subprocess.run(
            [sys.executable, "route_linter.py", "--backend", "./test_backend"],
            capture_output=True,
            text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required", result.stderr)
        
        # Test missing backend argument
        result = subprocess.run(
            [sys.executable, "route_linter.py", "--frontend", "./test_frontend"],
            capture_output=True,
            text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required", result.stderr)
    
    def test_successful_execution(self):
        """Test that the script runs successfully with both arguments"""
        result = subprocess.run(
            [sys.executable, "route_linter.py", "--backend", "./test_backend", "--frontend", "./test_frontend"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Backend path: ./test_backend", result.stdout)
        self.assertIn("Frontend path: ./test_frontend", result.stdout)

if __name__ == "__main__":
    # Create test directories if they don't exist
    os.makedirs("test_backend", exist_ok=True)
    os.makedirs("test_frontend", exist_ok=True)
    
    unittest.main()