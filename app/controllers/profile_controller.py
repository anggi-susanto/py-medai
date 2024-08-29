from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.profile_service import ProfileService
from app.models.user_model import UserSchema

profile_controller = Blueprint('profile_controller', __name__)
profile_service = ProfileService()
user_schema = UserSchema()

@profile_controller.route('/profile', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Profile'],
    'security': [
        {"bearerAuth": []},
    ],
    'responses': {
        '200': {
            'description': 'User profile',
            'content': {
                'application/json': {
                    'schema': {
                        '$ref': '#/components/schemas/User'
                    }
                }
            }
        },
        '404': {
            'description': 'User not found'
        }
    }
})
def get_profile():
    """
    Get user profile
    """
    username = get_jwt_identity()
    user = profile_service.get_profile(username)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_data = user_schema.dump(user)
    del user_data['password']
    return jsonify(user_data), 200


@profile_controller.route('/profile', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Profile'],
    'security': [
        {"bearerAuth": []},
    ],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    '$ref': '#/components/schemas/User'
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Updated user profile',
            'content': {
                'application/json': {
                    'schema': {
                        '$ref': '#/components/schemas/User'
                    }
                }
            }
        },
        '404': {
            'description': 'User not found'
        }
    }
})
def update_profile():
    """
    Update user profile
    """
    data = request.get_json()
    username = get_jwt_identity()
    user = profile_service.update_profile(
        username, data.get('name'), data.get('email'),
        data.get('phone'), data.get('profile_photo')
    )
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_data = user_schema.dump(user)
    return jsonify(user_data), 200
