from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_assets import Environment


db = SQLAlchemy()
migrate = Migrate()
manager = LoginManager()
assets = Environment()