from datetime import timezone
from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Notes(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(1500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    usr_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    notes = db.relationship('Notes')

    def get_id(self):
        return (self.user_id)