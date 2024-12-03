from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid


class Medication(db.Model):
    __tablename__ = 'medications'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    schedule = db.Column(db.String, nullable=False)
    appointment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('appointments.id'), nullable=False)  # FK
    user_id = db.Column(db.String, nullable=True)  # FK

    appointment = db.relationship('Appointment', back_populates='medications')
