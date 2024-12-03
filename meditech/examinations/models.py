from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid


class Examination(db.Model):
    __tablename__ = 'examinations'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    hospital_id = db.Column(UUID(as_uuid=True), db.ForeignKey('hospitals.id'), nullable=False)

    user = db.relationship('User', back_populates='examinations')
    hospital = db.relationship('Hospital', back_populates='examinations')
