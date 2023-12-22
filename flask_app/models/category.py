import uuid
from sqlalchemy.dialects.postgresql import UUID

from flask_app import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(35), unique=True, nullable=False)
    is_custom = db.Column(db.Boolean, unique=False, nullable=False)

    record = db.relationship("RecordModel", back_populates="category", lazy="dynamic")
    user_category = db.relationship("UserCategoryModel", back_populates="category", lazy="dynamic")
