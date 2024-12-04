from functools import wraps
from flask import request, jsonify
import jwt
from .users.models import User  # Import the User model
SECRET_KEY = 'roadtochina2025'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Tokens are sent in the 'Authorization' header
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # Decode the token
            data = jwt.decode(token.split(' ')[1], SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated