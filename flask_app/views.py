from flask_app import app


@app.route("/healthcheck")
def healthcheck():
    return "200"
