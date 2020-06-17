# fashion_wardrobe_tracker/users/forms.py
from flask_wtf import FlaskForm
from flask_login import current_user
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import fields
from wtforms.validators import Email, InputRequired, ValidationError

from .models import User


MEASUREMENTS = [
    (0, 'Metric'),
    (1, 'Imperial')
]


def get_measurement_pref():
    return MEASUREMENTS



class LoginForm(FlaskForm):
    email = fields.StringField(validators=[InputRequired(), Email()])
    password = fields.PasswordField(validators=[InputRequired()])

    # WTForms supports "inline" validators
    # which are methods of our `Form` subclass
    # with names in the form `validate_[fieldname]`.
    # This validator will run after all the
    # other validators have passed.
    def validate_password(self, field=None):
        try:
            user = User.query.filter(User.email == self.email.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user: none found")
        if user is None:
            raise ValidationError("Invalid user: none")
        if not user.is_valid_password(self.password.data):
            raise ValidationError("Invalid password")


        # Make the current user available
        # to calling code.
        self.user = user


class RegistrationForm(FlaskForm):
    name = fields.StringField("Display Name")
    email = fields.StringField(validators=[InputRequired(), Email()])
    password = fields.PasswordField(validators=[InputRequired()])
    imperial_preference = fields.SelectField('Measurement (preferred)',
                                        choices=get_measurement_pref(),
                                        default=0,
                                        coerce=int)

    def validate_email(form, field):
        user = User.query.filter(User.email == field.data).first()
        if user is not None:
            raise ValidationError("A user with that email already exists")



class UserProfileForm(FlaskForm):
    height = fields.IntegerField("Height (in cm)")
    weight = fields.IntegerField("Weight (in kg)")
    build = fields.SelectField('Build Type', default='short', coerce=str)
    shape = fields.SelectField('Build Shape', default='round', coerce=str)
    birthdate = fields.DateField('Birthday (MM/DD/YYYY)', format='%m/%d/%Y')
