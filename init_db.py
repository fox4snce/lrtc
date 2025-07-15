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
        
        # Create admin user
        from app import User
        from werkzeug.security import generate_password_hash
        
        admin = User(
            username='admin',
            email='admin@constitutiongame.com',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Database initialized successfully!")
        print("Admin user created: admin / admin123")

if __name__ == "__main__":
    init_database() 