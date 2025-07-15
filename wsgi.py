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

# Create a WSGI application that handles the subdirectory
class SubdirectoryMiddleware:
    def __init__(self, app, subdirectory):
        self.app = app
        self.subdirectory = subdirectory.rstrip('/')
    
    def __call__(self, environ, start_response):
        # Remove the subdirectory from the path
        if environ.get('PATH_INFO', '').startswith(self.subdirectory):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.subdirectory):]
            if not environ['PATH_INFO']:
                environ['PATH_INFO'] = '/'
        
        return self.app(environ, start_response)

# Apply the middleware for /lrtc subdirectory
application = SubdirectoryMiddleware(app, '/lrtc')

if __name__ == '__main__':
    app.run(debug=True) 