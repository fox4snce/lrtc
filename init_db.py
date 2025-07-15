#!/usr/bin/env python3
"""
Script to initialize the database with the correct schema.
"""

from app import app, db

def init_database():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        print("✅ Database initialized successfully!")
        print("Note: Use /setup_admin to create admin account with secure setup token.")

if __name__ == "__main__":
    init_database() 