import os
from flask import Flask, flash, request, redirect, url_for, Blueprint, jsonify, session
from werkzeug.utils import secure_filename
from flask import send_from_directory
from .models import User, File
from meditech.app import db
import uuid

users = Blueprint('users', __name__ )
ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

def getFilePath(user, category):
    return os.path.join(os.getcwd(), 'uploads', user, category)

@users.route('/uploads/<name>')
def download_file(name):
    # Get the user and find the file
    # receive also the category
    return send_from_directory(UPLOAD_FOLDER, name)

@users.route('/files', methods=['GET'])
def get_files_by_user_and_category():
    if 'email' not in request.args:
        return jsonify({'error': 'No email provided'}), 400
    if 'category' not in request.args:
        return jsonify({'error': 'No category provided'}), 400
    
    email = request.args.get('email')
    category = request.args.get('category')
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Query files by user and category
    files = File.query.filter_by(user_id=user.id, category=category).all()

    # Extract file names
    file_names = [file.name for file in files]

    return jsonify({category: file_names}), 200

@users.route('/files', methods=['POST'])
def upload_file():
    # Check for required parts of the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    if 'category' not in request.form:
        return jsonify({'error': 'No category'}), 400
    if 'email' not in request.form:
        return jsonify({'error': 'No email'}), 400
    
    file = request.files['file']
    email = request.form.get('email')
    category = request.form.get('category')

    # Validate the file
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    path = getFilePath(user.email, category)
    
    if file and allowed_file(file.filename):
        # Generate a random filename
        ext = os.path.splitext(file.filename)[1]  # Get the file extension
        random_name = f"{uuid.uuid4().hex}{ext}"
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        # Save the file with the random name
        full_path = os.path.join(path, secure_filename(random_name))
        file.save(full_path)

        # Optionally, save file details in the database
        new_file = File(
            name=random_name,
            category=category,
            user_id=user.id
        )
        db.session.add(new_file)
        db.session.commit()

        return jsonify({
            'message': 'File uploaded successfully'
        }), 201

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS