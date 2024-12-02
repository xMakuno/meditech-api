from flask import request, redirect, url_for, Blueprint

from meditech.users.models import User


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    age = request.form.get('age')