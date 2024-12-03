from flask import request, redirect, url_for, Blueprint, jsonify, session

from meditech.app import db
from meditech.doctors.models import Doctor

doctors = Blueprint('doctors', __name__, url_prefix='/doctors')


@doctors.route('/', methods=['GET'])
def get_all_doctors():
    doctors_list = Doctor.query.all()
    return jsonify([{
        'id': str(doctor.id),
        'name': doctor.name,
        'email': doctor.email,
        'phone': doctor.phone,
        'hospital': doctor.hospital,
        'specialty': doctor.specialty
    } for doctor in doctors_list])


@doctors.route('/<identifier>', methods=['GET'])
def get_doctor_by_id(identifier):
    """
    Endpoint to get a doctor by id
    Expects an identifier through Request Param
        -identifier: UUID of the Doctor
    """
    doctor = Doctor.query.get(identifier)
    if not doctor:
        return jsonify({'error': 'Doctor does not exists'}), 404

    return jsonify({
        'id': str(doctor.id),
        'name': doctor.name,
        'email': doctor.email,
        'phone': doctor.phone,
        'hospital': doctor.hospital,
        'specialty': doctor.specialty
    }), 200



@doctors.route('/', methods=['POST'])
def create_doctor():
    if request.content_type == 'application/json':
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        hospital = data.get('hospital')
        specialty = data.get('specialty')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        hospital = request.form.get('hospital')
        specialty = request.form.get('specialty')

    if Doctor.query.filter_by(email=email).first():
        return jsonify({'error': 'Doctor is already registered.'}), 409

    new_doctor = Doctor(
        name=name,
        email=email,
        phone=phone,
        hospital=hospital,
        specialty=specialty
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
                'hospital': new_doctor.hospital,
                'specialty': new_doctor.specialty
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to register doctor', 'details': str(e)}), 500
