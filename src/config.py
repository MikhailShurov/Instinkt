from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_JWT_KEY = os.environ.get("SECRET_JWT_KEY")
REDIS_PASS = os.environ.get("REDIS_PASS")