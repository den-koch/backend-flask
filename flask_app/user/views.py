from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound, IntegrityError

from . import user
from flask_app import app, db
from flask_app.models import UserModel
from flask_app.models.schemas import UserSchema

user_request_schema = UserSchema()
user_response_schema = UserSchema(only=("id", "user_name", "email"))


@user.route("/users", methods=["GET"])
def get_users():
    users = UserModel.query.all()

    json_users = user_response_schema.dump(users, many=True)

    return json_users, 200


@user.route("/users", methods=["POST"])
def create_user():
    json_data = request.get_json()

    try:
        data = user_request_schema.load(json_data)
    except ValidationError as err:
        return {"message": err.messages}, 400

    post_user = UserModel(user_name=data["user_name"], email=data["email"], password=data["password"])

    with app.app_context():
        db.session.add(post_user)
        db.session.commit()

        json_user = user_response_schema.dump(post_user)

        return json_user, 201


@user.route("/users/<string:user_id>", methods=["GET", "DELETE"])
def get_delete_user(user_id):
    if request.method == "GET":

        try:
            get_user = UserModel.query.filter_by(id=user_id).one()
        except NoResultFound:
            return {"message": f"User {user_id} not found"}, 404

        json_user = user_response_schema.dump(get_user)

        return json_user, 200

    if request.method == "DELETE":
        with app.app_context():
            try:
                delete_user = UserModel.query.filter_by(id=user_id).one()
            except NoResultFound:
                return {"message": f"User {user_id} not found"}, 204

            db.session.delete(delete_user)
            db.session.commit()

        return {"message": f"User {user_id} deleted"}, 200
