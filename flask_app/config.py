import os

PROPAGATE_EXCEPTIONS = True
FLASK_DEBUG = True
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
# SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
SQLALCHEMY_DATABASE_URI = "postgresql://flask_db_yv6s_user:hMOEuttjIVQti4eEfCIpEOaM0AIp5VZ8@dpg-cm28f7da73kc738kg990-a.oregon-postgres.render.com/flask_db_yv6s"
SQLALCHEMY_TRACK_MODIFICATIONS = False
API_TITLE = "Flask home accounting REST API"
API_VERSION = "v3"
OPENAPI_VERSION = "3.0.3"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
