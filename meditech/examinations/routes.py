from flask import request, redirect, url_for, Blueprint, jsonify, session
from flask_login import current_user
from meditech.app import db
from datetime import datetime

from .models import Examination
from ..appointments.models import Appointment
from ..doctors.models import Doctor
from ..hospitals.models import Hospital
from ..users.models import User
from ..token_req import token_required

examinations = Blueprint('examinations', __name__, url_prefix='/examinations')

@examinations.route('/self', methods=['GET'])
@token_required
def get_all_self_examinations(current_user):
    user_id = current_user.id
    examinations_list = Examination.query.filter(
        Examination.user_id == user_id,
    )
    return jsonify([{
        'id': examination.user_id,
        'name': examination.name,
        'date': examination.date,
        'hospital_id': examination.hospital_id,
        'user_id': examination.user_id
    } for examination in examinations_list]), 200


@examinations.route('/', methods=['POST'])
@token_required
def create_examination(current_user):

    """
    Endpoint to create an Examination
    Expects:
        -name: name of hospital
        -hospital_id: id of hospital
    """
    user_id = current_user.id
    if request.content_type == 'application/json':
        data = request.json
        name = data.get('name')
        hospital_id = data.get('')
    else:
        name = request.form.get('name')
        hospital_id = request.form.get('hospital_id')

    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        return jsonify({'error': 'Hospital not found!'}), 404

    new_examination = Examination(
        name=name,
        user_id=user_id,
        hospital_id=hospital_id,
        date=datetime.now().isoformat()
    )
    try:
        db.session.add(new_examination)
        db.session.commit()
        return jsonify({
            'message': 'Examination created successfully!',
            'examination': {
                'id': str(new_examination.id),
                'name': new_examination.name,
                'user_id': str(new_examination.user_id),
                'hospital_id': str(new_examination.hospital_id),
                'date': new_examination.date.isoformat()
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create appointment', 'details': str(e)}), 500


@examinations.route('/', methods=['GET'])
def get_all_examinations():
    examinations_list = Examination.query.all()
    return jsonify([{
        'id': examination.user_id,
        'name': examination.name,
        'date': examination.date,
        'hospital_id': examination.hospital_id,
        'user_id': examination.user_id
    } for examination in examinations_list]), 200
