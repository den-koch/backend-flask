from flask import Blueprint

user_category = Blueprint("user_category", __name__, url_prefix="/users/<string:user_id>")

from . import views