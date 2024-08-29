import os
from datetime import timedelta
from flask_jwt_extended import create_access_token as jwt_create_access_token
from flask_jwt_extended import create_refresh_token as jwt_create_refresh_token
from flask_jwt_extended import decode_token as jwt_decode_token

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

def generate_access_token(identity):
    return jwt_create_access_token(identity=identity, expires_delta=timedelta(minutes=15))

def generate_refresh_token(identity):
    return jwt_create_refresh_token(identity=identity, expires_delta=timedelta(days=30))

def decode_jwt_token(token):
    return jwt_decode_token(token, allow_expired=False)