from datetime import datetime as dt
from datetime import date

from passlib.hash import sha256_crypt
import random

from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from fashion_wardrobe_tracker.data import CRUDMixin, db
from fashion_wardrobe_tracker.wardrobe.models import Site, Visit, Upper


def utc_now():
    return dt.utcnow


class User(UserMixin, CRUDMixin, db.Model):
    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    profile = db.relationship("Profile", uselist=False, back_populates='user')

    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    imperial_preference = db.Column(db.Boolean, default=False, nullable=False) # metric vs imperial
    _password = db.Column(db.String(120))
    _clear_pw = db.Column(db.String(120))
    created_on = db.Column(db.DateTime, default=utc_now())
    modified_on = db.Column(db.DateTime, default=utc_now(), onupdate=utc_now())
    
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
        return f'<User ID: {self.id}>'


    def get_user_age(self):
        return Profile.query.filter(Profile.id==self.profile_id).first().get_age()


    def profile_exists(self):
        if self.profile:
            return True
        else:
            return False



class Profile(UserMixin, CRUDMixin, db.Model):
    __tablename__ = "users_profile"

    id = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users_user.id'))
    user = db.relationship("User", back_populates='profile')

    wardrobe = db.relationship('Wardrobe', back_populates='profile')
    
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    build = db.Column(db.String(120))
    shape = db.Column(db.String(120))
    birthdate = db.Column(db.Date)


    def get_age(self):
        today = date.today() 
        born = self.birthdate
        return today.year - born.year - (
                    (today.month, today.day) < (born.month, born.day)) 
 
    
    def __iter__(self):
        yield 'height', self.height
        yield 'weidght', self.weight
        yield 'build', self.build
        yield 'shape', self.shape
        yield 'birthdate', self.birthdate


    def __repr__(self):
        return f'<Profile ID: {self.id}>'