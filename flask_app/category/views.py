from flask import request
import uuid

from . import category
from ..models import Category

categories = {}


@category.route("/",methods=["GET", "POST"])
def get_create_categories():
    if request.method == "GET":
        return {category_id: category.__dict__ for category_id, category in categories.items()}
        # return categories

    if request.method == "POST":
        category_id = uuid.uuid4().hex
        new_category = Category(category_id=category_id, **request.get_json())
        categories[category_id] = new_category
        return new_category.__dict__


@category.route("/<string:category_id>", methods=["DELETE"])
def delete_category(category_id):
    if category_id not in categories.keys():
        return {"status": "204 (NO CONTENT)", "message": "Category not found"}

    del categories[category_id]
    return {"status": "200 (OK)", "message": "Category deleted"}
