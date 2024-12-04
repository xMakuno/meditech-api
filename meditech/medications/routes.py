from flask import request, redirect, url_for, Blueprint, jsonify, session
from flask_login import current_user
from .models import Medication
from meditech.app import db
from datetime import datetime
from ..token_req import token_required
from ..appointments.models import Appointment
from ..doctors.models import Doctor
from ..users.models import User

medications = Blueprint('medications', __name__, url_prefix='/medications')


@medications.route('/self', methods=['GET'])
@token_required
def get_self_active_medications(current_user):
    user_id = current_user.id
    medications_list = Medication.query.filter(
        Medication.user_id == user_id,
        Medication.active == True,
    )
    return jsonify([{
        'id': str(medication.id),
        'name': medication.name,
        'active': medication.active,
        'schedule': medication.schedule,
        'appointment_id': str(medication.appointment_id),
        'user_id': str(medication.user_id)
    } for medication in medications_list]), 200


@medications.route('/<medication_id>', methods=['PATCH'])
def toggle_pending_appointment(medication_id):
    try:
        medication = Medication.query.get(medication_id)
        if not medication:
            return jsonify({'error': 'Appointment not found!'}), 404

        medication.active = not medication.active
        db.session.commit()
        return jsonify({
            'message': 'Medication status updated successfully',
            'medication': {
                'id': str(medication.id),
                'name': medication.name,
                'active': medication.active,
                'schedule': medication.schedule,
                'appointment_id': str(medication.appointment_id),
                'user_id': str(medication.user_id)
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update appointment', 'details': str(e)}), 500


@medications.route('/', methods=['GET'])
def get_all_medications():
    medications_list = Medication.query.all()
    return jsonify([{
        'id': medication.id,
        'name': medication.name,
        'active': medication.active,
        'schedule': medication.schedule,
        'appointment_id': str(medication.appointment_id),
        'user_id': str(medication.user_id)
    } for medication in medications_list]), 200


@medications.route('/<appointment_id>', methods=['POST'])
@token_required
def create_medication(appointment_id):
    user_id = current_user.id
    if request.content_type == 'application/json':
        data = request.json
        name = data.get('name')
        schedule = data.get('schedule')
    else:
        name = request.form.get('name')
        schedule = request.form.get('schedule')

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'error': 'Appointment not found.'}), 404

    new_medication = Medication(
        name=name,
        schedule=schedule,
        appointment_id=appointment_id,
        user_id=user_id
    )

    try:
        db.session.add(new_medication)
        db.session.commit()
        return jsonify({
            'message': 'Medication created successfully',
            'medication': {
                'id': str(new_medication.id),
                'name': new_medication.name,
                'schedule': new_medication.schedule,
                'active': new_medication.active,
                'appointment_id': str(new_medication.appointment_id),
                'user_id': str(new_medication.user_id)
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create appointment', 'details': str(e)}), 500

