from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py", silent=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import flask_app.views

# app blueprints

from .user import user as user_blueprint

app.register_blueprint(user_blueprint)

from .category import category as category_blueprint

app.register_blueprint(category_blueprint)

from .record import record as record_blueprint

app.register_blueprint(record_blueprint)
