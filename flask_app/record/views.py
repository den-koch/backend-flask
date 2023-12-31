from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import UUID
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from . import record
from flask_app import app, db
from flask_app.models import RecordModel, CategoryModel, UserCategoryModel
from flask_app.models.schemas import RecordSchema

record_schema = RecordSchema()


@record.route("/records", methods=["GET"])
@jwt_required()
def get_records():
    user_id = get_jwt_identity()
    category_id = request.args.get("category_id")

    if not user_id and not category_id:
        return {"message": "Required parameters are not specified"}, 400

    if category_id:
        records = RecordModel.query.filter_by(user_id=user_id, category_id=category_id)
    else:
        records = RecordModel.query.filter_by(user_id=user_id)

    json_records = record_schema.dump(records, many=True)

    return json_records, 200


@record.route("/records", methods=["POST"])
@jwt_required()
def create_record():
    json_data = request.get_json()

    try:
        data = record_schema.load(json_data)
    except ValidationError as err:
        return {"message": err.messages}, 400

    user_id, category_id = get_jwt_identity(), data['category_id']

    category = CategoryModel.query.filter_by(id=category_id).first()
    if not category:
        return {"message": f"Category {category_id} not found"}, 404

    if category.is_custom:
        user_category = UserCategoryModel.query.filter_by(user_id=user_id, category_id=category_id).first()
        if not user_category:
            return {"message": "Category does not belong to the user"}, 400

    post_record = RecordModel(user_id=user_id, category_id=category_id,
                              date_time=data["date_time"], amount=data["amount"])

    with app.app_context():
        db.session.add(post_record)
        db.session.commit()

        json_record = record_schema.dump(post_record)

    return json_record, 201


@record.route("/records/<string:record_id>", methods=["GET", "DELETE"])
@jwt_required()
def get_delete_record(record_id):
    current_user_id = get_jwt_identity()

    if request.method == "GET":
        try:
            get_record = RecordModel.query.filter_by(id=record_id).one()
        except NoResultFound:
            return {"message": f"Record {record_id} not found"}, 404

        if get_record.user_id != UUID(current_user_id):
            return {'message': 'Unauthorized'}, 403

        json_record = record_schema.dump(get_record)

        return json_record, 200

    if request.method == "DELETE":
        with app.app_context():
            try:
                delete_record = RecordModel.query.filter_by(id=record_id).one()
            except NoResultFound:
                return {"message": f"User {record_id} not found"}, 204

            if delete_record.user_id != UUID(current_user_id):
                return {'message': 'Unauthorized'}, 403

            db.session.delete(delete_record)
            db.session.commit()

            return {"message": f"Record {record_id} deleted"}, 200
