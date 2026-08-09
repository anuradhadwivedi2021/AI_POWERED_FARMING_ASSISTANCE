import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


def _build_db_uri():
    """
    Local dev  → SQL Server (SSMS, Windows Auth)
    Production → PostgreSQL (Render managed DB), via DATABASE_URL env var

    Render apne aap DATABASE_URL environment variable set kar deta hai
    jab tum uske saath ek Postgres database attach karte ho — us case mein
    yeh function seedha wahi URL use kar lega, SQL Server wala code chalega hi nahi.
    """
    direct_url = os.environ.get('DATABASE_URL')
    if direct_url:
        # Render kabhi-kabhi purana 'postgres://' scheme deta hai,
        # SQLAlchemy 2.0 ko 'postgresql://' chahiye
        if direct_url.startswith('postgres://'):
            direct_url = direct_url.replace('postgres://', 'postgresql://', 1)
        return direct_url

    db_server = os.environ.get('DB_SERVER', r'LENOVO\SQLEXPRESS01')
    db_name   = os.environ.get('DB_NAME', 'farming_assistant')
    db_driver = os.environ.get('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    auth_mode = os.environ.get('DB_AUTH_MODE', 'windows')  # 'windows' or 'sql'

    if auth_mode == 'sql':
        db_user = os.environ.get('DB_USER', '')
        db_pass = os.environ.get('DB_PASSWORD', '')
        odbc_str = (
            f"DRIVER={{{db_driver}}};SERVER={db_server};DATABASE={db_name};"
            f"UID={db_user};PWD={db_pass};TrustServerCertificate=yes;"
        )
    else:
        # Windows Authentication — koi username/password nahi chahiye
        odbc_str = (
            f"DRIVER={{{db_driver}}};SERVER={db_server};DATABASE={db_name};"
            f"Trusted_Connection=yes;TrustServerCertificate=yes;"
        )

    return f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_str)}"


class Config:
    SECRET_KEY         = os.environ.get('SECRET_KEY') or 'cropsense-secret-2024'
    SQLALCHEMY_DATABASE_URI = _build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
    }
    UPLOAD_FOLDER      = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    WEATHER_API_KEY    = os.environ.get('WEATHER_API_KEY') or ''
    GEMINI_API_KEY     = os.environ.get('GEMINI_API_KEY') or ''