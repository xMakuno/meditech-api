from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid

"""
    Initial:
    -id: default to uuid()
    -reason: required (json/form)
    -date: default to now()
    -user_id: required (through auth)
    -doctor_id: required (json/form)
    -pending: default to True
    -hospital_id: defaults to doctor's hospital
    
    Lazy:
    -heart_rate: modified by Doctor
    -blood_pressure: modified by Doctor
    -weight: modified by Doctor
    -recommendations: modified by Doctor
"""


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String, nullable=False)
    pending = db.Column(db.Boolean, nullable=False, default=True)
    doctor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('doctors.id'), nullable=False)  # FK
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)  # FK
    hospital_id = db.Column(UUID(as_uuid=True), db.ForeignKey('hospitals.id'), nullable=False)  # FK

    heart_rate = db.Column(db.String, nullable=True)
    blood_pressure = db.Column(db.String, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    recommendations = db.Column(db.String, nullable=True)

    user = db.relationship('User', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')
    hospital = db.relationship('Hospital', back_populates='appointments')

    medications = db.relationship('Medication', back_populates='appointment', cascade='all, delete-orphan')
