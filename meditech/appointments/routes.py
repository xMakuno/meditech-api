from flask import request, redirect, url_for, Blueprint, jsonify, session
from flask_login import login_required, current_user

from meditech.app import db
from meditech.appointments.models import Appointment
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
    if request.content_type == 'application/json':
        data = request.json
        date_str = data.get('date')
        notes = data.get('notes', '')  # Notes are optional
    else:
        date_str = request.form.get('date')
        notes = request.form.get('notes', '')

    # Validate the required fields
    if not date_str or not user_id:
        return jsonify({'error': 'The date and user_id fields are required'}), 400

    try:
        # Convert date string to a datetime.date object
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Retrieve the user from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Create a new appointment instance
    new_appointment = Appointment(
        date=appointment_date,
        notes=notes,
        user_id=user.id  # Link appointment to user
    )

    # Add and commit the new appointment to the database
    try:
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({
            'message': 'Appointment created successfully',
            'appointment': {
                'id': str(new_appointment.id),  # UUID is serialized as a string
                'date': new_appointment.date.isoformat(),
                'notes': new_appointment.notes,
                'user_id': str(new_appointment.user_id)
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create appointment', 'details': str(e)}), 500