from flask import request
import uuid

from . import record
from ..models import Record

records = {}


@record.route("/", methods=["GET"])
def get_records():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")

    if not user_id and not category_id:
        return {"message": "Required parameters are not specified"}, 400

    filter = records
    if user_id:
        filter = {record_id: record for record_id, record in filter.items() if
                  record.user_id == user_id}
    if category_id:
        filter = {record_id: record for record_id, record in filter.items() if
                  record.category_id == category_id}

    return {record_id: record.__dict__ for record_id, record in filter.items()}


@record.route("/", methods=["POST"])
def create_record():
    record_id = uuid.uuid4().hex
    new_record = Record(record_id=record_id, **request.get_json())
    records[record_id] = new_record
    return new_record.__dict__


@record.route("/<string:record_id>", methods=["GET", "DELETE"])
def get_delete_record(record_id):
    if request.method == "GET":
        if record_id not in records.keys():
            return {"status": "404 (NOT FOUND)", "message": "Record not found"}
        return {record_id: records[record_id].__dict__}

    if request.method == "DELETE":
        if record_id not in records.keys():
            return {"status": "204 (NO CONTENT)", "message": "Record not found"}
        del records[record_id]
        return {"status": "200 (OK)", "message": "Record deleted"}
