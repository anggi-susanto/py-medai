import os
from flask import Flask, send_from_directory
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config.config import Config
from app import create_app, db 
from pathlib import Path
UPLOAD_FOLDER = '/static/uploads/'
app = create_app()

# Initialize database

# Initialize JWT
jwt = JWTManager(app)

# Initialize Migrate
migrate = Migrate(app, db)

# Swagger configuration using OpenAPI 3
swagger_config = {
    "openapi": "3.0.0",
    "info": {
        "title": "My API",
        "version": "1.0.0",
        "description": "API documentation using OpenAPI 3",
    },
    "headers": [],  # Ensure this is defined as an empty list if not used
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            },
            
            "refreshToken": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            },
        },
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                    "profile_photo": {"type": "string"}
                }
            },
            "UserUpdate": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                }
            },
            "Login": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["username", "password"]
            },
            "Token": {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "refresh_token": {"type": "string"}
                }
            }
        }
    },
    "security": [
        {
            "bearerAuth": [],
            "refreshToken": []
        }
    ],
    "servers": [
        {
            "url": "http://127.0.0.1:5000",
            "description": "Local development server"
        }
    ],
    "tags": [
        {
            "name": "Authentication",
            "description": "Endpoints related to user authentication"
        },
        {
            "name": "Profile",
            "description": "Endpoints related to user profile management"
        }
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)

# Register Blueprints
from app.controllers.auth_controller import auth_controller
from app.controllers.profile_controller import profile_controller

app.register_blueprint(auth_controller, url_prefix='/api/v1/auth')
app.register_blueprint(profile_controller, url_prefix='/api/v1')
@app.route('/static/uploads/profile_photos/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_photos'), filename)

if __name__ == '__main__':
    app.run(debug=True)