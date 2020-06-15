from datetime import datetime as dt
from passlib.hash import sha256_crypt
import random

from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from fashion_wardrobe_tracker.data import CRUDMixin, db
from fashion_wardrobe_tracker.tracking.models import Site, Visit


def utc_now():
    return dt.utcnow


class User(UserMixin, CRUDMixin, db.Model):
    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    imperial_preference = db.Column(db.Boolean, default=False, nullable=False) # metric vs imperial
    _password = db.Column(db.String(120))
    _clear_pw = db.Column(db.String(120))
    created_on = db.Column(db.DateTime, default=utc_now())
    modified_on = db.Column(db.DateTime, default=utc_now(), onupdate=utc_now())
    # wardrobe = db.relationship('wardrobe', backref='owner', lazy='dynamic')

    @hybrid_property
    def password(self):
        return self._password


    @password.setter
    def password(self, pw_input):
        rounds = current_app.config.get("HASH_ROUNDS")
        self._password = sha256_crypt.hash(pw_input, rounds=rounds)
        if current_app.config.get("ENV") == 'Development':
            self._clear_pw = pw_input
        

    def is_valid_password(self, pw):
        return sha256_crypt.verify(pw, self._password)


    def __repr__(self):
        return f'<User #{self.id}>'
