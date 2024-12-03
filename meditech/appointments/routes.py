from flask import request, redirect, url_for, Blueprint, jsonify, session
from flask_login import login_required, current_user

from meditech.app import db
from meditech.appointments.models import Appointment
from meditech.doctors.models import Doctor
from meditech.users.models import User
from datetime import datetime

appointments = Blueprint('appointments', __name__ )


@appointments.route('/pending/<appointment_id>', methods=['PATCH'])
def toggle_pending_appointment(appointment_id):
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found!'}), 404

        appointment.pending = not appointment.pending
        db.session.commit()
        return jsonify({
            'message': 'Appointment status updated successfully',
            'appointment': {
                'id': str(appointment.id),
                'date': appointment.date.isoformat(),
                'reason': appointment.reason,
                'user_id': str(appointment.user_id),
                'doctor_id': appointment.doctor_id,
                'pending': appointment.pending
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update appointment', 'details': str(e)}), 500


@appointments.route('/<doctor_id>', methods=['GET'])
def get_appointments_by_doctor_id(doctor_id):
    appointments_list = Appointment.query.get(doctor_id=doctor_id)
    return jsonify([{
        'id': str(appointment.id),
        'date': appointment.date.isoformat(),
        'reason': appointment.reason,
        'user_id': str(appointment.user_id),
        'doctor_id': appointment.doctor_id,
        'pending': appointment.pending
    } for appointment in appointments_list]), 200


@appointments.route('/pending/<doctor_id>', methods=['GET'])
def get_pending_appointments_by_doctor_id(doctor_id):
    appointments_list = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.pending == True
    ).all()
    return jsonify([{
        'id': str(appointment.id),
        'date': appointment.date.isoformat(),
        'reason': appointment.reason,
        'user_id': str(appointment.user_id),
        'doctor_id': appointment.doctor_id,
        'pending': appointment.pending
    } for appointment in appointments_list]), 200


@appointments.route('/self')
@login_required
def get_self_appointments():
    user_id = current_user.id
    appointments_list = Appointment.query.filter_by(user_id=user_id)
    return jsonify([{
        'id': str(appointment.id),
        'date': appointment.date.isoformat(),
        'reason': appointment.reason,
        'user_id': str(appointment.user_id),
        'doctor_id':  appointment.doctor_id,
        'pending': appointment.pending
    } for appointment in appointments_list]), 200


@appointments.route('/', methods=['GET'])
def get_all():
    appointments_list = Appointment.query.all()
    # If you want to return a proper JSON response with appointment details
    return jsonify([{
        'id': str(appointment.id),
        'date': appointment.date.isoformat(),
        'reason': appointment.reason,
        'user_id': str(appointment.user_id),
        'doctor_id': appointment.doctor_id,
        'pending': appointment.pending
    } for appointment in appointments_list])


# TODO: Edit Appointment back to how it was
@appointments.route('/', methods=['POST'])
@login_required
def create_appointment():
    """
    Endpoint to create a new appointment.
    Supports both JSON and form-encoded payloads.
    Expects:
    - reason: reason for the appointment
    - doctor_id: patients desired doctor
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
        reason = data.get('reason')
        doctor_id = data.get('doctor_id')
    else:
        reason = request.form.get('reason')
        doctor_id = request.form.get('doctor_id')

    # Retrieve the user from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    print(doctor)
    # TODO: Update the instantiation of new appointment
    # Create a new appointment instance
    new_appointment = Appointment(
        doctor_id=doctor.id,
        date=datetime.now().isoformat(),
        user_id=user.id,  # Link appointment to user
        reason=reason
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
                'reason': new_appointment.reason,
                'date': new_appointment.date.isoformat(),
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create appointment', 'details': str(e)}), 500
