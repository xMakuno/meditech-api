import os
from flask import Flask, flash, request, redirect, url_for, Blueprint, jsonify, session
from werkzeug.utils import secure_filename
from flask import send_from_directory
from .models import User, File, FileShare
from meditech.app import db
from ..token_req import token_required
import uuid

users = Blueprint('users', __name__ )
ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

def getFilePath(user, category=""):
    return os.path.join(os.getcwd(), 'uploads', user, category)

@users.route('/uploads/<name>')
@token_required
def download_file(current_user, name):
    return send_from_directory(getFilePath(current_user.email), name)

@users.route('/doctor/files')
@token_required
def get_shared_files(current_user):
    if 'category' not in request.args:
        return jsonify({'error': 'No category provided'}), 400
    if 'patient' not in request.args:
        return jsonify({'error': 'No patient provided'}), 400

    category = request.args.get('category')
    patient = request.args.get('patient')

    user = User.query.filter_by(email=patient).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    files = File.query.join(FileShare, FileShare.file_id == File.id).filter(FileShare.shared_with_id == current_user.id, File.category == category, FileShare.shared_by_id == user.id).all()
    file_list = [{'name': file.name, 'date': file.created_at} for file in files]
    return jsonify({'files': file_list}), 200


@users.route('/share', methods=['POST'])
@token_required
def share_files(current_user):
    doctor_email = request.json.get('doctor_email')
    # share all files with doctor_email to share it should use the FileShare model
    if not doctor_email:
        return jsonify({'error': 'Doctor email is required'}), 400
    user = User.query.filter_by(email=doctor_email).first()
    if not user:
        return jsonify({'error': 'Doctor not found'}), 404
    files = File.query.filter_by(user_id=current_user.id).all()
    for file in files:
        new_share = FileShare(
            file_id=file.id,
            shared_by_id=current_user.id,
            shared_with_id=user.id
        )
        db.session.add(new_share)
    db.session.commit()
        
    return jsonify({'message': 'Files shared successfully'}), 200

@users.route('/userfiles', methods=['GET'])
@token_required
def get_files_by_user(current_user):
    user_id = current_user.id

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Query files by user and category
    files = File.query.filter_by(user_id=user.id).all()

    # Extract file names
    file_list = [{'name': file.name, 'date': file.created_at} for file in files]

    return jsonify({'files': file_list}), 200

@users.route('/files', methods=['GET'])
@token_required
def get_files_by_user_and_category(current_user):
    user_id = current_user.id

    if 'category' not in request.args:
        return jsonify({'error': 'No category provided'}), 400
    
    category = request.args.get('category')
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Query files by user and category
    files = File.query.filter_by(user_id=user.id, category=category).all()

    # Extract file names
    file_list = [{'name': file.name, 'date': file.created_at} for file in files]

    return jsonify({'files': file_list}), 200

@users.route('/uploadfile', methods=['POST'])
@token_required
def upload_file(current_user):
    user_id = current_user.id
    # Check for required parts of the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    if 'category' not in request.form:
        return jsonify({'error': 'No category'}), 400
    
    file = request.files['file']
    category = request.form.get('category')

    # Validate the file
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    path = getFilePath(user.email)
    
    if file and allowed_file(file.filename):
        # Generate a random filename
        # ext = os.path.splitext(file.filename)[1]  # Get the file extension
        # random_name = f"{uuid.uuid4().hex}{ext}"
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        # Save the file with the random name
        full_path = os.path.join(path, file.filename)
        file.save(full_path)

        # Optionally, save file details in the database
        new_file = File(
            name=file.filename,
            category=category,
            user_id=user.id
        )
        db.session.add(new_file)
        db.session.commit()

        return jsonify({
            'message': 'File uploaded successfully'
        }), 201

@users.route('/')
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        if ("doctor" not in user.email):
            user_data = {
                'id': str(user.id),
                'email': user.email,
            }
            output.append(user_data)
    return jsonify({'patients': output}), 200



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS