from flask import Blueprint, request, jsonify, session
from flask_login import login_user, login_required
from .models import Insurance
from meditech.app import db

insurances = Blueprint('insurances', __name__, url_prefix='/insurances')


@insurances.route('/', methods=['GET'])
def get_all_insurances():
    insurances_list = Insurance.query.all()
    return jsonify([{
        'id': insurance.id,
        'name': insurance.name
    } for insurance in insurances_list]), 200
