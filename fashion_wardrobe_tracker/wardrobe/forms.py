from datetime import datetime as dt

from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Site


class SiteForm(FlaskForm):
    base_url = fields.StringField(validators=[Required()])


class VisitForm(FlaskForm):
    browser = fields.StringField()
    date = fields.DateField(default=dt.now)
    event = fields.StringField()
    url = fields.StringField(validators=[Required()])
    ip_address = fields.StringField()
    location = fields.StringField()
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    site = QuerySelectField(validators=[Required()], query_factory=lambda: Site.query.all())



class UppersForm(FlaskForm):
    name = fields.StringField(
                label="Name this Upper", validators=[Required()])
    brand = fields.SelectField(
                label='Brand', validators=[Required()])
    style = fields.SelectField(
                label='Style', validators=[Required()])
    size = fields.SelectField(
                label='Size', validators=[Required()])
    year = fields.IntegerField(
                label='Year - optional')
    pattern = fields.SelectField(
                label='Pattern', validators=[Required()])
    color1 = fields.SelectField(
                label='Color (Primary)', validators=[Required()])
    color2 = fields.SelectField(
                label='Color (Secondary) - optional')
    color3 = fields.SelectField(
                label='Color (Accent) - optional')
    fit = fields.SelectField(
                label='Fit', validators=[Required()])
    material = fields.SelectField(
                label='Material / Fabric', validators=[Required()])
    stretch = fields.RadioField(
                label='Stretch', default="no")



class LowersForm(FlaskForm):
    name = fields.StringField(
                label="Name this Lower", validators=[Required()])
    brand = fields.SelectField(
                label='Brand', validators=[Required()])
    style = fields.SelectField(
                label='Style', validators=[Required()])
    waist = fields.IntegerField(
                label='Waist', validators=[Required()])
    inseam = fields.IntegerField(
                label='Inseam', validators=[Required()])
    year = fields.IntegerField(
                label='Year - optional')
    pattern = fields.SelectField(
                label='Pattern', validators=[Required()])
    color1 = fields.SelectField(
                label='Color (Primary)', validators=[Required()])
    color2 = fields.SelectField(
                label='Color (Secondary) - optional')
    color3 = fields.SelectField(
                label='Color (Accent) - optional')
    fit = fields.SelectField(
                label='Fit', validators=[Required()])
    material = fields.SelectField(
                label='Material / Fabric', validators=[Required()])
    stretch = fields.RadioField(
                label='Stretch', default="no")



class FootersForm(FlaskForm):
    name = fields.StringField(
                label="Name these Shoes", validators=[Required()])
    brand = fields.StringField(
                label='Brand', validators=[Required()])
    style = fields.StringField(
                label='Style', validators=[Required()])
    size = fields.DecimalField(
                label='Shoe Size', validators=[Required()])
    year = fields.IntegerField(
                label='Year - optional')
    pattern = fields.SelectField(
                label='Pattern', validators=[Required()])
    color1 = fields.SelectField(
                label='Color (Primary)', validators=[Required()])
    color2 = fields.SelectField(
                label='Color (Secondary) - optional')
    color3 = fields.SelectField(
                label='Color (Accent) - optional')
    fit = fields.SelectField(
                label='Fit', validators=[Required()])
    material = fields.SelectField(
                label='Material / Fabric', validators=[Required()])


class WardrobeForm(FlaskForm):
    name = fields.StringField(label="Name this Wardrobe",
                                validators=[Required()])

    uppers = fields.FormField(UppersForm)
    lowers = fields.FormField(LowersForm)
    footers = fields.FormField(FootersForm)