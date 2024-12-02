from flask import request, redirect, url_for, Blueprint, jsonify, session

from meditech.app import db
from meditech.doctors.models import Doctor

doctors = Blueprint('doctors', __name__ )


@doctors.route('/', methods=['GET'])
def get_all_doctors():
    doctors_list = Doctor.query.all()
    return jsonify([{
        'id': str(doctor.id),
        'name': doctor.name,
        'email': doctor.email,
        'phone': doctor.phone,
        'hospital': doctor.hospital
    } for doctor in doctors_list])

@doctors.route('/', methods=['POST'])
def create_doctor():
    if request.content_type == 'application/json':
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        hospital = data.get('hospital')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        hospital = request.form.get('hospital')

    if Doctor.query.filter_by(email=email).first():
        return jsonify({'error': 'Doctor is already registered.'}), 409

    new_doctor = Doctor(
        name=name,
        email=email,
        phone=phone,
        hospital=hospital
    )
    try:
        db.session.add(new_doctor)
        db.session.commit()
        return jsonify({
            'message': 'Doctor registered successfully',
            'doctor': {
                'id': str(new_doctor.id),
                'name': new_doctor.name,
                'email': new_doctor.email,
                'phone': new_doctor.phone,
                'hospital': new_doctor.hospital
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to register doctor', 'details': str(e)}), 500