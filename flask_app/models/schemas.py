from marshmallow import Schema, fields, validate, validates, ValidationError
from flask_app.models import CategoryModel


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_name = fields.String(required=True)
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.String(required=True, load_only=True)


class RecordSchema(Schema):
    id = fields.UUID(dump_only=True)
    # user_id = fields.UUID(required=True)
    category_id = fields.UUID(required=True)
    date_time = fields.DateTime(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0.0))


class CategorySchema(Schema):
    id = fields.UUID(dump_only=True)
    category_name = fields.String(required=True)
    is_custom = fields.Boolean(dump_only=True)

    @validates("category_name")
    def validate_category_name(self, category_name):
        if CategoryModel.query.filter_by(category_name=category_name).first() is not None:
            raise ValidationError("Category already exists")


class UserCategorySchema(Schema):
    id = fields.UUID(dump_only=True)
    # user_id = fields.UUID(required=True)
    category_id = fields.UUID(required=True)