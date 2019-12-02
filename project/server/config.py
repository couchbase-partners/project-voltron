import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13    


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4

