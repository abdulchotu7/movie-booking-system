"""
Configuration settings for the application.
"""
import os

# Database configuration
DATABASE_URL = "postgresql://postgres.xugmfazmoxlkkwhfhxyl:capstone@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

# Application settings
SECRET_KEY = "your-secret-key-32-chars-long"
DEBUG = True

# Templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
