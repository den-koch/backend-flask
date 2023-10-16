from flask_app import app

from datetime import datetime


@app.route("/healthcheck")
def healthcheck():
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    response = {
        "status": "200 OK",
        "date": current_datetime
    }
    return response
