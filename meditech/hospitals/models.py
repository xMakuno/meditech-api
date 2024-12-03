from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid


class Hospital(db.Model):
    __tablename__ = 'hospitals'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    appointments = db.relationship('Appointment', back_populates='hospital', cascade='all, delete-orphan')
    examinations = db.relationship('Examination', back_populates='hospital', cascade='all, delete-orphan')

