from ..extensions import db
from .channels import Channels


class Packs(db.Model):
    __tablename__ = 'packs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channels = db.relationship(Channels, backref='packs', lazy='dynamic')
    pack_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
