from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import NoResultFound

from . import user
from flask_app import app, db
from flask_app.models import UserModel
from flask_app.models.schemas import UserSchema

user_signup_schema = UserSchema()
user_signin_schema = UserSchema(only=("email", "password"))
user_response_schema = UserSchema(only=("id", "user_name", "email"))


@user.route("/users", methods=["GET"])
def get_users():
    users = UserModel.query.all()

    json_users = user_response_schema.dump(users, many=True)

    return json_users, 200


@user.route("/users/signup", methods=["POST"])
def user_signup():
    json_data = request.get_json()

    try:
        data = user_signup_schema.load(json_data)

        if UserModel.query.filter_by(email=data["email"]).first() is not None:
            raise ValidationError("Email already exists")

    except ValidationError as err:
        return {"message": err.messages}, 400



    post_user = UserModel(user_name=data["user_name"], email=data["email"],
                          password=pbkdf2_sha256.hash(data["password"]))

    with app.app_context():
        db.session.add(post_user)
        db.session.commit()

        json_user = user_response_schema.dump(post_user)

        return json_user, 201


@user.route("/users/signin", methods=["POST"])
def user_signin():
    json_data = request.get_json()

    try:
        data = user_signin_schema.load(json_data)
    except ValidationError as err:
        return {"message": err.messages}, 400

    get_user = UserModel.query.filter_by(email=data["email"]).first()

    if get_user and pbkdf2_sha256.verify(data["password"], get_user.password):
        access_token = create_access_token(identity=get_user.id)
        return {"access_token": access_token}, 200
    else:
        return {"message": "Bad email or password"}, 401


@user.route("/users/<string:user_id>", methods=["GET", "DELETE"])
@jwt_required()
def get_delete_user(user_id):
    current_user_id = get_jwt_identity()
    if user_id != current_user_id:
        return {'message': 'Unauthorized'}, 403

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
