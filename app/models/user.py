from flask_login import UserMixin
from ..extensions import db, manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(128), nullable=True)
    lastname = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    plan = db.Column(db.String(128), nullable=True)


@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
