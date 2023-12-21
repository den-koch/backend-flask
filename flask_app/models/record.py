import uuid
from sqlalchemy.dialects.postgresql import UUID

from flask_app import db


class RecordModel(db.Model):
    __tablename__ = "records"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), unique=False, nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey("categories.id"), unique=False, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float(precision=2), unique=False, nullable=False)

    user = db.relationship("UserModel", back_populates="record")
    category = db.relationship("CategoryModel", back_populates="record")
