from os import getenv
from dotenv import load_dotenv

load_dotenv()  

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'tu_clave_jwt_secreta'
