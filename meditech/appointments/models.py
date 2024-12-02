from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    date = db.Column(db.Date, nullable=False)
    # Foreign key to USERS table
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    # Foreign key to DOCTORS table
    doctor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('doctors.id'), nullable=False)

    notes = db.Column(db.String, nullable=True)
    heart_rate = db.Column(db.String, nullable=True)  # Optional, could be Integer if needed
    blood_pressure = db.Column(db.String, nullable=True)  # Optional, could be a more specific type
    medication = db.Column(db.String, nullable=True)  # Optional
    weight = db.Column(db.Float, nullable=True)  # Optional
    pending = db.Column(db.Boolean, nullable=False, default=True)
    # Relationship to User
    user = db.relationship('User', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')

    def __repr__(self):
        return f"<Appointment {self.id}, User {self.user_id}, Date {self.date}, Pending {self.pending}>"