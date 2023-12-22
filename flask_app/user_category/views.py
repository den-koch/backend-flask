from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from . import user_category
from flask_app import app, db
from flask_app.models import UserCategoryModel, CategoryModel, UserModel
from flask_app.models.schemas import UserCategorySchema, CategorySchema

category_request_schema = CategorySchema()
category_response_schema = CategorySchema(only=("id", "category_name"))


@user_category.route("/user-categories", methods=["GET"])
def get_user_categories(user_id):
    try:
        user = UserModel.query.filter_by(id=user_id).one()
    except NoResultFound:
        return {"message": f"User {user_id} not found"}, 404

    user_categories = UserCategoryModel.query.filter_by(user_id=user_id).all()

    user_category_ids = [category.category_id for category in user_categories]

    categories = CategoryModel.query.filter(CategoryModel.id.in_(user_category_ids)).all()

    json_categories = category_response_schema.dump(categories, many=True)

    return json_categories, 200


@user_category.route("/user-categories", methods=["POST"])
def create_user_category(user_id):
    try:
        user = UserModel.query.filter_by(id=user_id).one()
    except NoResultFound:
        return {"message": f"User {user_id} not found"}, 404

    json_data = request.get_json()

    try:
        data = category_request_schema.load(json_data)
    except ValidationError as err:
        return {"message": err.messages}, 400

    post_category = CategoryModel(category_name=data["category_name"], is_custom=True)

    with app.app_context():
        db.session.add(post_category)
        db.session.commit()

        json_category = category_response_schema.dump(post_category)

    post_user_category = UserCategoryModel(user_id=user_id, category_id=post_category.id)

    with app.app_context():
        db.session.add(post_user_category)
        db.session.commit()

    return json_category, 201


@user_category.route("/user-categories/<string:user_category_id>", methods=["DELETE"])
def delete_category(user_id, user_category_id):
    try:
        user = UserModel.query.filter_by(id=user_id).one()
    except NoResultFound:
        return {"message": f"User {user_id} not found"}, 404

    with app.app_context():
        try:
            user_category = UserCategoryModel.query.filter_by(user_id=user_id, category_id=user_category_id).one()
            delete_user_category = CategoryModel.query.filter_by(id=user_category_id, is_custom=True).one()
        except NoResultFound:
            return {"message": f"User category {user_category_id} not found"}, 204

        db.session.delete(user_category)
        db.session.delete(delete_user_category)
        db.session.commit()

        return {"message": f"User category {user_category_id} deleted"}, 200
