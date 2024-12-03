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
    upload_path = db.Column(db.String(100), nullable=False)
    
    # Relationships
    appointments = db.relationship('Appointment', back_populates='user', cascade='all, delete-orphan')
    subscriptions = db.relationship('Subscription', back_populates='user', cascade='all, delete-orphan')
    examinations = db.relationship('Examination', back_populates='user', cascade='all, delete-orphan')
    files = db.relationship('File', back_populates='user', cascade='all, delete-orphan')  # Add this line

    def __repr__(self):
        return f"<User {self.name}>"

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='files')  # Keep this line
