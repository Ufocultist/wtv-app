from ..extensions import db


class Channels(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    channel_name = db.Column(db.String(128), nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(256), nullable=True)
    pack = db.Column(db.Integer, db.ForeignKey('packs.id', ondelete='CASCADE'))

