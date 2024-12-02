from flask import request, redirect, url_for, Blueprint, jsonify

from meditech.app import db
from meditech.appointments.models import Appointment
from datetime import datetime

appointments = Blueprint('appointments', __name__ )


@appointments.route('/', methods=['GET'])
def get_all():
    appointments_list = Appointment.query.all()
    return appointments_list

@appointments.route('/', methods=['POST'])
def create_appointment():
    """
    Endpoint to create a new appointment.
    Supports both JSON and form-encoded payloads.
    Expects:
    - date: The date of the appointment in 'YYYY-MM-DD' format.
    - notes: Optional notes for the appointment.
    """
    # Check for form data or JSON
    if request.content_type == 'application/json':
        data = request.json
        date_str = data.get('date')
        notes = data.get('notes', '')  # Notes are optional
    else:
        date_str = request.form.get('date')
        notes = request.form.get('notes', '')

    # Validate the required date field
    if not date_str:
        return jsonify({'error': 'The date field is required'}), 400

    try:
        # Convert date string to a datetime.date object
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Create a new appointment instance
    new_appointment = Appointment(
        date=appointment_date,
        notes=notes
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
                'notes': new_appointment.notes
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create appointment', 'details': str(e)}), 500
