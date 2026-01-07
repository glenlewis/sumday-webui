import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SUMDAY_DATABASE_URL') or 'postgresql://localhost/sumday_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Auth0 Configuration
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    AUTH0_CALLBACK_URL = os.environ.get('AUTH0_CALLBACK_URL') or 'http://classic.kisa.com:5555/callback'
    AUTH0_AUDIENCE = f"https://{os.environ.get('AUTH0_DOMAIN')}/userinfo"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}