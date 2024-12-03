import os
from flask import Flask, flash, request, redirect, url_for, Blueprint, jsonify, session
from werkzeug.utils import secure_filename
from flask import send_from_directory
from .models import User

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

@users.route('/file', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        if 'category' not in request.form:
            return jsonify({'error': 'No category'}), 400
        if 'email' not in request.form:
            return jsonify({'error': 'No email'}), 400
        
        file = request.files['file']
        email = request.form.get('email')
        category = request.form.get('category')

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        user = User.query.filter_by(email=email).first()
        path = getFilePath(user.email, category)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            if not os.path.exists(path):
                os.makedirs(path)
            file.save(path)
            return redirect(url_for('users.upload_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS