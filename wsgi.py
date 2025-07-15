#!/usr/bin/env python3
"""
WSGI entry point for the constitutional game application.
This file handles the /lrtc subdirectory deployment.
"""

import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# Simple and working subdirectory middleware
class SubdirectoryMiddleware:
    def __init__(self, app, subdirectory):
        self.app = app
        self.subdirectory = subdirectory
    
    def __call__(self, environ, start_response):
        # Check if the path starts with our subdirectory
        path_info = environ.get('PATH_INFO', '')
        
        if path_info.startswith(self.subdirectory):
            # Remove the subdirectory from PATH_INFO
            environ['PATH_INFO'] = path_info[len(self.subdirectory):]
            # If PATH_INFO is empty, set it to '/'
            if not environ['PATH_INFO']:
                environ['PATH_INFO'] = '/'
            # Set SCRIPT_NAME to the subdirectory
            environ['SCRIPT_NAME'] = self.subdirectory
        
        return self.app(environ, start_response)

# Apply the middleware
application = SubdirectoryMiddleware(app, '/lrtc')

if __name__ == '__main__':
    app.run(debug=True) 