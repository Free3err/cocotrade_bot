import os
import logging


class AppConfig:
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    API_HOST = os.getenv('API_HOST')
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGINS = ['http://localhost:3000', os.getenv('API_HOST')]


class DatabaseConfig:
    DATABASE_URI = os.path.join(AppConfig.BASE_DIR, "instance", "db", "cocotrade.db")


class LoggingConfig:
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logging.addLevelName(logging.INFO, '\033[32m[INFO]\033[0m')
    logging.addLevelName(logging.WARNING, '\033[33m[WARNING]\033[0m')
    logging.addLevelName(logging.ERROR, '\033[31m[ERROR]\033[0m')
    logging.addLevelName(logging.CRITICAL, '\033[91m[CRITICAL]\033[0m')
