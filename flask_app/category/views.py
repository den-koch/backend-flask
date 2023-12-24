from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from . import category
from flask_app import app, db
from flask_app.models import CategoryModel, RecordModel
from flask_app.models.schemas import CategorySchema

category_request_schema = CategorySchema()
category_response_schema = CategorySchema(only=("id", "category_name"))


@category.route("/categories", methods=["GET", "POST"])
@jwt_required()
def get_create_categories():
    if request.method == "GET":
        categories = CategoryModel.query.filter_by(is_custom=False).all()

        json_categories = category_response_schema.dump(categories, many=True)

        return json_categories, 200

    if request.method == "POST":

        json_data = request.get_json()

        try:
            data = category_request_schema.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, 400

        post_category = CategoryModel(category_name=data["category_name"], is_custom=False)

        with app.app_context():
            db.session.add(post_category)
            db.session.commit()

            json_category = category_response_schema.dump(post_category)

        return json_category, 201


@category.route("/categories/<string:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    with app.app_context():

        category_record = RecordModel.query.filter_by(category_id=category_id).first()
        if not category_record:
            return {"message": f"Category {category_id} in use"}, 403

        try:
            delete_category = CategoryModel.query.filter_by(id=category_id, is_custom=False).one()
        except NoResultFound:
            return {"message": f"Category {category_id} not found"}, 204

        db.session.delete(delete_category)
        db.session.commit()

        return {"message": f"Category {category_id} deleted"}, 200
