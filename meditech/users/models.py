from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)  # To store hashed passwords
    birthdate = db.Column(db.Date, nullable=False)
