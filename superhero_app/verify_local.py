import sys
import os

print("Verifying setup...")

try:
    import fastapi
    import uvicorn
    import sqlalchemy
    import requests
    import jinja2
    print("Dependencies ok.")
except ImportError as e:
    print(f"Missing dependency: {e}")
    # We might not be able to proceed but let's see.

try:
    from app import models, database, crud, schemas
    print("Imports ok.")
    
    # Try to create DB
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=database.engine)
    print("Database tables created.")
    
    # Verify DB file exists
    if os.path.exists("./superhero.db"):
        print("superhero.db found.")
    else:
        print("Error: superhero.db not found after creation.")
        
except Exception as e:
    print(f"Error during app verification: {e}")
