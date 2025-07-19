from flask import Flask
from sqlalchemy import exc
from .bundles import bundles, register_bundles
from .extensions import db, migrate, manager, assets
from .config import Config
from .routes.user import user
from .routes.channels import channel
from .routes.packs import pack
from .routes.main import main


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(user)
    app.register_blueprint(channel)
    app.register_blueprint(pack)
    app.register_blueprint(main)

    db.init_app(app)
    migrate.init_app(app, db)
    manager.init_app(app)
    assets.init_app(app)

    # Login Manager
    manager.login_view = 'user.login_page'
    manager.login_message = 'Please log in to access this page'
    manager.login_message_category = 'info'

    # Assets
    register_bundles(assets, bundles)

    with app.app_context():
        try:
            db.create_all()
        except exc.SQLAlchemyError as sqlalchemyerror:
            print(sqlalchemyerror)
        except Exception as exception:
            print(exception)
        finally:
            print("No exceptions were raised")
    return app
