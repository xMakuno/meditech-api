from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    hospital = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    specialty = db.Column(db.String, nullable=False)

    # Relationships
    appointments = db.relationship('Appointment', back_populates='doctor', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Doctor {self.name}, Hospital: {self.hospital}, Specialty: {self.specialty}>"

