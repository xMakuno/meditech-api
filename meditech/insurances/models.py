from meditech.app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Insurance(db.Model):
    __tablename__ = 'insurances'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)

    subscriptions = db.relationship('Subscription', back_populates='insurance', cascade='all, delete-orphan')
