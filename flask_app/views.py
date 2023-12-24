from flask import jsonify

from flask_app import app, jwt

from datetime import datetime


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@app.route("/healthcheck")
def healthcheck():
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    response = {
        "status": "200 OK",
        "date": current_datetime
    }
    return response
