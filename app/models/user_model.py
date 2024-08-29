from marshmallow import Schema, fields
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_photo = db.Column(db.String(255))

    def __init__(self, name, username, email, phone, password, profile_photo=None):
        self.name = name
        self.username = username
        self.email = email
        self.phone = phone
        self.password = password
        self.profile_photo = profile_photo

class UserSchema(Schema):
    user_id = fields.Int(attribute='id')
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    profile_photo = fields.Str()
    password = fields.Str(required=True)

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class TokenSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()

# Swagger definitions
user_schema = UserSchema()

# To be used by Flasgger
definitions = {
    "User": UserSchema,
    "Login": LoginSchema,
    "Token": TokenSchema
}