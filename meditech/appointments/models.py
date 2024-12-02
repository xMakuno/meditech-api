from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String)