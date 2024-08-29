from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flasgger import swag_from
from app.services.auth_service import AuthService
from app.models.user_model import LoginSchema, TokenSchema, UserSchema

auth_controller = Blueprint('auth_controller', __name__)
auth_service = AuthService()
login_schema = LoginSchema()
token_schema = TokenSchema()
user_schema = UserSchema()

@auth_controller.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    '$ref': '#/components/schemas/User'
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'User created successfully',
            'content': {
                'application/json': {
                    'schema': {
                        '$ref': '#/components/schemas/User'
                    }
                }
            }
        },
        '400': {
            'description': 'Invalid input'
        }
    }
})
def register():
    """
    Register a new user
    """
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    try:
        user = auth_service.register_user(
            name=data['name'],
            username=data['username'],
            email=data['email'],
            phone=data['phone'],
            password=data['password'],
            profile_photo=data.get('profile_photo')
        )
        

        # Serialize the user entity to a dictionary with the correct format
        user_data = user_schema.dump(user)
        del user_data['password']

        return jsonify(user_data), 201
    except Exception as e:
        return jsonify({'message': 'something went wrong'}), 500

@auth_controller.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    '$ref': '#/components/schemas/Login'
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'JWT Token',
            'content': {
                'application/json': {
                    'schema': {
                        '$ref': '#/components/schemas/Token'
                    }
                }
            }
        },
        '401': {
            'description': 'Invalid credentials'
        }
    }
})
def login():
    data = request.get_json()
    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Attempt to log in the user
    result = auth_service.login(data['username'], data['password'])
    
    # Handle the case where login fails
    if result is None:
        return jsonify({"message": "Invalid credentials"}), 401

    # Unpack the tokens from the service result
    access_token, refresh_token = result

    # Return the tokens in the response
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@auth_controller.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@swag_from({
    'tags': ['Authentication'],
    'security': [
        {"refreshToken": []},
    ],
    'responses': {
        '200': {
            'description': 'New JWT access token',
            'schema': {
                '$ref': '#/components/schemas/Token'
            }
        },
        '401': {
            'description': 'Invalid refresh token'
        }
    }
})
def refresh():
    """
    Refresh JWT Token
    """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200