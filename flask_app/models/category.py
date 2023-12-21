import uuid
from sqlalchemy.dialects.postgresql import UUID

from flask_app import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(35), unique=True, nullable=False)

    record = db.relationship("RecordModel", back_populates="category", lazy="dynamic")
