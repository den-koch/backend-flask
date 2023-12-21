import uuid
from sqlalchemy.dialects.postgresql import UUID

from flask_app import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    record = db.relationship("RecordModel", back_populates="user", lazy="dynamic")
