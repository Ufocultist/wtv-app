import os


class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/uploads'
    SERVER_PATH = ROOT + UPLOAD_PATH

    USER = os.environ.get('DB_USERNAME', 'smotrish_user')
    PASSWORD = os.environ.get('DB_PASSWORD', 'ia2xwbbyby')
    HOST = os.environ.get('DB_HOST', 'mariadb')
    PORT = os.environ.get('DB_PORT', '3306')
    DB = os.environ.get('DB_NAME', 'smotrish_db')

    SQLALCHEMY_DATABASE_URI = f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'adsadaydoi38dhiu7w87dys7tasye2u7y77&@#3jd8UDOUD*#EDasdsaded3ss'
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 1800,  # Recycle connections after 30 minutes
        "pool_pre_ping": True  # Check connection before using it
    }
