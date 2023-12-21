from flask import request

from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from . import record
from flask_app import app, db
from flask_app.models import RecordModel
from flask_app.models.schemas import RecordSchema

record_schema = RecordSchema()


@record.route("/records", methods=["GET"])
def get_records():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")

    if not user_id and not category_id:
        return "Required parameters are not specified", 400

    if user_id:
        if category_id:
            records = RecordModel.query.filter_by(user_id=user_id, category_id=category_id)
        else:
            records = RecordModel.query.filter_by(user_id=user_id)
    else:
        records = RecordModel.query.filter_by(category_id=category_id)

    json_records = record_schema.dump(records, many=True)

    return json_records, 200


@record.route("/records", methods=["POST"])
def create_record():
    json_data = request.get_json()

    try:
        data = record_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 400

    post_record = RecordModel(user_id=data["user_id"], category_id=data["category_id"],
                              date_time=data["date_time"], amount=data["amount"])

    with app.app_context():
        db.session.add(post_record)
        db.session.commit()

        json_record = record_schema.dump(post_record)

    return json_record, 201


@record.route("/records/<string:record_id>", methods=["GET", "DELETE"])
def get_delete_record(record_id):
    if request.method == "GET":
        try:
            get_record = RecordModel.query.filter_by(record_id=record_id).one()
        except NoResultFound:
            return f"Record {record_id} not found", 404

        json_record = record_schema.dump(get_record)

        return json_record, 200

    if request.method == "DELETE":
        with app.app_context():
            try:
                delete_record = RecordModel.query.filter_by(record_id=record_id).one()
            except NoResultFound:
                return f"User {record_id} not found", 204

            db.session.delete(delete_record)
            db.session.commit()

            return f"Record {record_id} deleted", 200
