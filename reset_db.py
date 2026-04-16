import os
from app import app
from models import db

def reset_database():
    """
    Deletes the existing SQLite database files and recreates them
    to ensure the new schema and constraints (like ON DELETE CASCADE) 
    are properly applied.
    """
    db_paths = [
        'escuela.db',
        'instance/escuela.db',
        'instance/proyecto.db'
    ]
    
    print("--- Resetting Database ---")
    for path in db_paths:
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"Deleted: {path}")
            except Exception as e:
                print(f"Error deleting {path}: {e}")

    with app.app_context():
        db.create_all()
        print("Database tables recreated successfully.")
    print("--------------------------")

if __name__ == "__main__":
    reset_database()
