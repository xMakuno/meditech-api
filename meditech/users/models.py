from flask_login import UserMixin  # Import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid
from datetime import datetime

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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # New attribute
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='files')  # Keep this line


class FileShare(db.Model):
    __tablename__ = 'file_shares'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = db.Column(UUID(as_uuid=True), db.ForeignKey('files.id'), nullable=False)
    shared_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    shared_with_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    file = db.relationship('File', backref=db.backref('shares', lazy=True))
    shared_by = db.relationship('User', foreign_keys=[shared_by_id], backref=db.backref('shared_files', lazy=True))
    shared_with = db.relationship('User', foreign_keys=[shared_with_id], backref=db.backref('received_files', lazy=True))

    def __repr__(self):
        return f"<FileShare file_id={self.file_id} shared_by={self.shared_by_id} shared_with={self.shared_with_id}>"