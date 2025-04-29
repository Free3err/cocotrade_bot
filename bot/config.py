import dotenv
import logging
import os


class EnvConfig:
    dotenv.load_dotenv()

    TOKEN = os.getenv("TOKEN")
    API_HOST = os.getenv("API_HOST")
    SECRET_KEY = os.getenv("SECRET_KEY")


class LoggingConfig:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logging.addLevelName(logging.INFO, '\033[32m[INFO]\033[0m')
    logging.addLevelName(logging.WARNING, '\033[33m[WARNING]\033[0m')
    logging.addLevelName(logging.ERROR, '\033[31m[ERROR]\033[0m')
    logging.addLevelName(logging.CRITICAL, '\033[91m[CRITICAL]\033[0m')
