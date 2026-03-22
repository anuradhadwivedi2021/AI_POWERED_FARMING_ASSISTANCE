import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kisan-ai-secret-2024'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///farming.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    WEATHER_API_KEY = os.environ.get('4d87fbccfbdca1fa6acc4d44d7f44064') or ''
    GEMINI_API_KEY = os.environ.get('') or ''