from prince import db
from datetime import datetime

class Language(db.Model):
    __tablename__='prince_language'
    id = db.Column(db.Integer, primary_key=True)
    iso = db.Column(db.Text, unique=True, nullable=False)
    varpron = db.Column(db.Integer)
    french = db.Column(db.Text, nullable=False)
    english = db.Column(db.Text, nullable=False)
    self = db.Column(db.Text)
    text = db.Column(db.Text)
    imgtext = db.Column(db.String(20))
    trad = db.Column(db.String(120))
    comment = db.Column(db.Text)
    actif = db.Column(db.Integer)
    grp = db.Column(db.Integer)
    geo = db.Column(db.String(100))
    geolat = db.Column(db.Float)
    geolng = db.Column(db.Float)

    def __repr__(self):
        return f"Langue('{self.french}')"

class Sound(db.Model):
    __tablename__='prince_sound'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(11))
    speaker = db.Column(db.Text)
    language = db.Column(db.Text)
    comment = db.Column(db.Text)
    private = db.Column(db.Text)

class Group(db.Model):
    __tablename__='prince_grp'
    i = db.Column(db.Integer, primary_key=True)
    grp = db.Column(db.Text)

class Relation(db.Model):
    __tablename__='prince_grp_rel'
    parent = db.Column(db.Integer, primary_key=True)
    child = db.Column(db.Integer)
