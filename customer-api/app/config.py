import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / '.env')

DATABASE_URL = os.getenv('SUPABASE_DATABASE_URL') or os.getenv('DATABASE_URL') or 'sqlite:///./smart_ecommerce.db'
DEV_MODE = os.getenv('DEV_MODE', 'true').lower() == 'true'
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_API_AUDIENCE = os.getenv('AUTH0_API_AUDIENCE')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
EMAIL_PROVIDER = os.getenv('EMAIL_PROVIDER', 'console')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:3000',
    FRONTEND_URL,
]
