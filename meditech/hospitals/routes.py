from flask import request, redirect, url_for, Blueprint, jsonify, session
from flask_login import login_required, current_user

from meditech.app import db
from .models import Hospital
from datetime import datetime

hospitals = Blueprint('hospitals', __name__, url_prefix='/hospitals')


@hospitals.route('/<hospital_id>', methods=['GET'])
def get_hospital_by_id(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        return jsonify({'error': 'Hospital not found!'}), 404
    return jsonify({
        'id': hospital.id,
        'name': hospital.name,
        'location': hospital.location,
    }), 200

@hospitals.route('/', methods=['GET'])
def get_all_hospitals():
    hospitals_list = Hospital.query.all()
    return jsonify([{
        'id': hospital.id,
        'name': hospital.name,
        'location': hospital.location
    } for hospital in hospitals_list]), 200
