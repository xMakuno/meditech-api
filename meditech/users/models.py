from sqlalchemy.dialects.postgresql import UUID
from meditech.app import db
import uuid

class User(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)