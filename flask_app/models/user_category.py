import uuid
from sqlalchemy.dialects.postgresql import UUID

from flask_app import db


class UserCategoryModel(db.Model):
    __tablename__ = "user_categories"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), unique=False, nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey("categories.id"), unique=False, nullable=False)

    category = db.relationship("CategoryModel", back_populates="user_category")
    user = db.relationship("UserModel", back_populates="user_category")
