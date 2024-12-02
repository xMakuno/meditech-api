from flask_login import UserMixin  # Import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    # Relationship to Appointment
    appointments = db.relationship('Appointment', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.name}>"