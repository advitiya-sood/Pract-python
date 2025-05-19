import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = os.getenv('FLASK_JWT_SECRET_KEY')

