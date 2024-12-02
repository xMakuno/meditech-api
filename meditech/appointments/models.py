from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)  # Foreign key to USERS table

    # Relationship to User
    user = db.relationship('User', back_populates='appointments')

    def __repr__(self):
        return f"<Appointment {self.id}, User {self.user_id}>"