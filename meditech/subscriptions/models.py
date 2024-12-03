from meditech.app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)  # FK
    insurance_id = db.Column(UUID(as_uuid=True), db.ForeignKey('insurances.id'), nullable=False)  # FK

    user = db.relationship('User', back_populates='subscriptions')
    insurance = db.relationship('Insurance', back_populates='subscriptions')

