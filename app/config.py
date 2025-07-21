import os


class Config(object):
    APPNAME = os.environ.get('APP_NAME', '.')
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = os.environ.get('UPLOAD_PATH', '/app/static/uploads')
    SERVER_PATH = UPLOAD_PATH

    USER = os.environ.get('DB_USERNAME')
    PASSWORD = os.environ.get('DB_PASSWORD')
    HOST = os.environ.get('DB_HOST', 'localhost')
    PORT = os.environ.get('DB_PORT', '3306')
    DB = os.environ.get('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'True').lower() == 'true'

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": int(os.environ.get("SQLALCHEMY_POOL_RECYCLE", "1800")),
        "pool_pre_ping": os.environ.get("SQLALCHEMY_POOL_PRE_PING", "true").lower() == "true"
    }