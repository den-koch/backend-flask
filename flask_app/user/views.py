from flask import request
import uuid

from . import user
from ..models import User

users = {}


@user.route("/", methods=["GET"])
def get_users():
    return {user_id: user.__dict__ for user_id, user in users.items()}


@user.route("/", methods=["POST"])
def create_user():
    user_id = uuid.uuid4().hex
    new_user = User(user_id=user_id, **request.get_json())
    users[user_id] = new_user
    return new_user.__dict__


@user.route("/<string:user_id>", methods=["GET", "DELETE"])
def get_delete_user(user_id):
    if request.method == "GET":
        if user_id not in users.keys():
            return {"status": "404 (NOT FOUND)", "message": "User not found"}
        return {user_id: users[user_id].__dict__}

    if request.method == "DELETE":
        if user_id not in users.keys():
            return {"status": "204 (NO CONTENT)", "message": "User not found"}
        del users[user_id]
        return {"status": "200 (OK)", "message": "User deleted"}
