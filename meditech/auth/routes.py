from flask import Blueprint, request, jsonify, session
from flask_login import login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from meditech.users.models import User
from meditech.doctors.models import Doctor
from meditech.app import db
from datetime import datetime, timedelta
import jwt

auth = Blueprint('auth', __name__, url_prefix='/auth')

SECRET_KEY = 'roadtochina2025'

@auth.route('/register', methods=['POST'])
def register():
    """
    Endpoint to register a new user.
    Expects a JSON/Form payload with:
    - email: User's email (unique).
    - password: User's password (plaintext, will be hashed).
    - birthdate: Birthdate in YYYY-MM-DD format.
    """
    data = request.json

    # Extract and validate input
    email = data.get('email')
    password = data.get('password')
    birthdate_str = data.get('birthdate')
    upload_path = data.get('email')

    if not email or not password or not birthdate_str:
        return jsonify({'error': 'Email, password, and birthdate are required.'}), 400

    try:
        # Convert birthdate string to date object
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid birthdate format. Use YYYY-MM-DD.'}), 400

    # Check if the email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email is already registered.'}), 409

    # Hash the password
    password_hash = generate_password_hash(password)

    # Create a new user instance
    new_user = User(
        email=email,
        password=password_hash,
        birthdate=birthdate,
        upload_path=upload_path
    )

    if "doctor" in email:
        new_doctor = Doctor(
            email=email,
            name=email.split('@')[0],
            hospital="Hospital",
            phone="1234567890",
            specialty="General"
        )
        db.session.add(new_doctor)
        db.session.commit()

    # Add the user to the database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message': 'User registered successfully.',
            'user': {
                'id': str(new_user.id),
                'email': new_user.email,
                'birthdate': new_user.birthdate.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to register user.', 'details': str(e)}), 500

@auth.route('/login', methods=['POST'])
def login():
    """
    Endpoint to authenticate a user.
    Expects a JSON payload with:
    - email: User's registered email.
    - password: User's plaintext password.
    """
    # Check for form data or JSON
    if request.content_type == 'application/json':
        data = request.json
        email = data.get('email')
        password = data.get('password')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

    # TODO: redirect if email == "quemado"

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    # Retrieve the user from the database
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Invalid email or password.'}), 401

    # Verify the password
    if not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid email or password.'}), 401

    # Store user session details
    login_user(user)
    token = jwt.encode(
        {
            'user_id': str(user.id),
            'exp': datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        },
        SECRET_KEY,
        algorithm='HS256'
    )
    return jsonify({
        'message': 'Login successful',
        'user': {
            'token':token,
            'email': user.email
        }
    }), 200