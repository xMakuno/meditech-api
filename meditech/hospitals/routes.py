from flask import request, redirect, url_for, Blueprint, jsonify, session
from flask_login import login_required, current_user

from meditech.app import db
from .models import Hospital
from datetime import datetime

hospitals = Blueprint('hospitals', __name__, url_prefix='/hospitals')


@hospitals.route('/', methods=['GET'])
def get_all_hospitals():
    hospitals_list = Hospital.query.all()
    return jsonify([{
        'id': hospital.id,
        'name': hospital.name,
        'location': hospital.location
    } for hospital in hospitals_list]), 200
