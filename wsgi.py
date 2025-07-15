#!/usr/bin/env python3
"""
WSGI entry point for the constitutional game application.
The app.py file now handles the /lrtc subdirectory routing.
"""

import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# The app already has the subdirectory middleware configured
application = app

if __name__ == '__main__':
    app.run(debug=True) 