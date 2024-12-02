from flask import request, redirect, url_for, Blueprint, jsonify, session
from flask_login import login_required, current_user

from meditech.app import db
from meditech.appointments.models import Appointment
from meditech.doctors.models import Doctor
from meditech.users.models import User
from datetime import datetime

appointments = Blueprint('appointments', __name__ )


@appointments.route('/', methods=['GET'])
def get_all():
    appointments_list = Appointment.query.all()
    # If you want to return a proper JSON response with appointment details
    return jsonify([{
        'id': str(appointment.id),
        'date': appointment.date.isoformat(),
        'notes': appointment.notes,
        'user_id': str(appointment.user_id)
    } for appointment in appointments_list])


@appointments.route('/self')
@login_required
def get_self_appointments():
    user_id = current_user.id
    appointments_list = Appointment.query.filter_by(user_id=user_id)
    return jsonify([{
        'id': str(appointment.id),
        'date': appointment.date.isoformat(),
        'notes': appointment.notes,
        'user_id': str(appointment.user_id)
    } for appointment in appointments_list])


@appointments.route('/', methods=['POST'])
def create_appointment():
    """
    Endpoint to create a new appointment.
    Supports both JSON and form-encoded payloads.
    Expects:
    - date: The date of the appointment in 'YYYY-MM-DD' format.
    - notes: Optional notes for the appointment.
    - user_id: The user ID (foreign key to USERS table).
    """
    print(f"Session: {session}")
    print(f"Current User: {current_user}")
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return jsonify({'error': 'User is not authenticated.'}), 401

    # Check for form data or JSON
    # Use current_user to get the logged-in user
    user_id = current_user.id  # Get logged-in user’s ID
    # TODO: Update info to match the Appointment model
    if request.content_type == 'application/json':
        data = request.json
        notes = data.get('notes', '')  # Notes are optional
        medication = data.get('medication', '')  # Medication is optional
        heart_rate = data.get('heart_rate', '')  # Heart Rate is optional
        blood_pressure = data.get('blood_pressure', '')  # Blood Pressure is optional
        weight = data.get('weight', 0.00)  # Weight is optional
        doctor_id = data.get('doctor_id')
    else:
        notes = request.form.get('notes', '')
        medication = request.form.get('medication', '')
        heart_rate = request.form.get('heart_rate', '')
        blood_pressure = request.form.get('blood_pressure', '')
        weight = request.form.get('weight', 0.00)
        doctor_id = request.form.get('doctor_id')

    # Retrieve the user from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404

    # TODO: Update the instantiation of new appointment
    # Create a new appointment instance
    new_appointment = Appointment(
        doctor_id=doctor_id,
        date=datetime.now().isoformat(),
        user_id=user.id,  # Link appointment to user
        notes=notes,
        medication=medication,
        heart_rate=heart_rate,
        blood_pressure=blood_pressure,
        weight=weight
    )

    # Add and commit the new appointment to the database
    try:
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({
            'message': 'Appointment created successfully',
            'appointment': {
                'id': str(new_appointment.id),  # UUID is serialized as a string
                'user_id': str(new_appointment.user_id),
                'doctor_id': str(new_appointment.doctor_id),
                'notes': new_appointment.notes,
                'medication': new_appointment.medication,
                'heart_rate': new_appointment.heart_rate,
                'blood_pressure': new_appointment.blood_pressure,
                'weight': new_appointment.weight
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create appointment', 'details': str(e)}), 500
