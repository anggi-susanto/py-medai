# config/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__)).replace("config", "")
class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = (
        "mysql+mysqlconnector://"+DATABASE_URL
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret-key")
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads/') 