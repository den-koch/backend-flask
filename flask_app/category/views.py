from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound, IntegrityError

from . import category
from flask_app import app, db
from flask_app.models import CategoryModel
from flask_app.models.schemas import CategorySchema

category_schema = CategorySchema()


@category.route("/categories", methods=["GET", "POST"])
def get_create_categories():
    if request.method == "GET":
        categories = CategoryModel.query.all()

        json_categories = category_schema.dump(categories, many=True)

        return json_categories, 200

    if request.method == "POST":

        json_data = request.get_json()

        try:
            data = category_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        post_category = CategoryModel(category_name=data["category_name"])

        with app.app_context():
            db.session.add(post_category)
            db.session.commit()

            json_category = category_schema.dump(post_category)

        return json_category, 201


@category.route("/categories/<string:category_id>", methods=["DELETE"])
def delete_category(category_id):
    with app.app_context():
        try:
            delete_category = CategoryModel.query.filter_by(id=category_id).one()
        except NoResultFound:
            return {"message": f"Category {category_id} not found"}, 204

        db.session.delete(delete_category)
        db.session.commit()

        return {"message": f"Category {category_id} deleted"}, 200
