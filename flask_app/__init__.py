from flask import Flask

app = Flask(__name__)

import flask_app.views

# app blueprints

from .user import user as user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")

from .category import category as category_blueprint
app.register_blueprint(category_blueprint, url_prefix="/categories")

from .record import record as record_blueprint
app.register_blueprint(record_blueprint, url_prefix="/records")
