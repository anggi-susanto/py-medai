from flask import Blueprint, request, jsonify, send_from_directory, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.profile_service import ProfileService
from app.models.user_model import UserSchema
from werkzeug.utils import secure_filename
import os

profile_controller = Blueprint('profile_controller', __name__)
profile_service = ProfileService()
user_schema = UserSchema()
UPLOAD_FOLDER = 'static/uploads/profile_photos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Define allowed extensions
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
                    '$ref': '#/components/schemas/UserUpdate'
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
    del user_data['password']
    return jsonify(user_data), 200

@profile_controller.route('/profile/photo', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Profile'],
    'security': [
        {"bearerAuth": []},
    ],
    'requestBody': {
        'required': True,
        'content': {
            'multipart/form-data': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'profile_photo': {
                            'type': 'string',
                            'format': 'binary'
                        }
                    }
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Profile photo uploaded successfully',
            'content': {
                'application/json': {
                    'schema': {
                        '$ref': '#/components/schemas/User'
                    }
                }
            }
        },
        '400': {
            'description': 'Invalid file format or other errors'
        }
    }
})
def upload_profile_photo():
    """
    Upload profile photo
    """
    if 'profile_photo' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['profile_photo']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Generate the image URL
        image_url = url_for('static', filename=f'uploads/profile_photos/{filename}', _external=True)
        
        username = get_jwt_identity()
        user = profile_service.update_profile(
            username, None, None, None, image_url
        )
        if not user:
            return jsonify({"message": "User not found"}), 404
        user_data = user_schema.dump(user)
        del user_data['password']
        return jsonify(user_data), 200

    return jsonify({"message": "Invalid file format"}), 400

