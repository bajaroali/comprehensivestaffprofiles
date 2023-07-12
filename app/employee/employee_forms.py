from flask_wtf import FlaskForm
from wtforms import StringField, FileField, EmailField, SelectField, RadioField, IntegerField, DateField, TextAreaField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField, QueryRadioField
from app.models import db, Employee, Rank, Section, Region, County, Subcounty, Tribe, Gender


class EmployeeBiodataForm(FlaskForm):
    service_number = IntegerField('Service number', validators=[DataRequired()])
    pf_number = IntegerField('Pf number', validators=[DataRequired()])
    id_number = IntegerField ('National id', validators=[DataRequired()])
    tax_pin = StringField('KRA pin', validators=[DataRequired(),Length(11)])
    gender =QueryRadioField('Gender', query_factory=lambda:Gender.query.all(), get_label="name", validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    middle_name = StringField('Middle name')
    last_name = StringField('Last name', validators=[DataRequired()])
    tribe = QuerySelectField('Tribe', query_factory=lambda: Tribe.query.order_by(Tribe.name.desc()).all(), get_label="name", allow_blank=True, blank_text="click to select..")
    dob = DateField('Date of birth', validators=[DataRequired()])
    blood_group = StringField('Blood group')
    identification_marks = TextAreaField('Bodily identifation marks')
    height = DecimalField('Height in inches', places=2)
    face_shape = StringField('Face Shape')
    transferin_date = DateField('Transfer in date',validators=[DataRequired()])
    enlistment_date = DateField('Enlistment date', validators=[DataRequired()])
    confirmation_date = DateField('Date confirmed', validators=[DataRequired()])
    rank = SelectField('Select rank', coerce=int)
    section = SelectField ('Section of deployment', validators=[DataRequired()])
    submit= SubmitField('Submit')

    def __init__(self, *args, **kwargs):
      super(EmployeeBiodataForm, self).__init__(*args, **kwargs)
      self.rank.choices = [(rank.id, rank.name) for rank in Rank.query.order_by(Rank.id).all()]
      self.section.choices =[(section.id, section.name) for section in Section.query.order_by(Section.name).all()]
    
    def validate_service_number(self, field):
      if  Employee.query.filter_by(service_number=field.data).first():
         raise ValidationError('Service number has to be unique.')
    
    def validate_pf_number(self, field):
      if  Employee.query.filter_by(pf_number=field.data).first():
         raise ValidationError('Pf number has to be unique.')
    
    def validate_id_number(self, field):
      if  Employee.query.filter_by(id_number=field.data).first():
         raise ValidationError('ID number has to be unique.')
    
    def validate_tax_pin(self, field):
      if  Employee.query.filter_by(tax_pin=field.data).first():
         raise ValidationError('KRA pin has to be unique.')

class EmployeeHomeAndContactDetailsForm(FlaskForm):
    primary_mobile = IntegerField('Primary mobile number', validators=[DataRequired("This is a required field.")])
    alternate_mobile = IntegerField('Alternate mobile')
    email = EmailField ('Working email', validators=[DataRequired(), Email()])
    postal_address = TextAreaField ('Permanent Address', validators=[DataRequired()])
    region = QuerySelectField('Region', query_factory=lambda: Region.query.all(), allow_blank=True, get_label="name", blank_text="select..")
    county = QuerySelectField('County', get_label="name", allow_blank=True, blank_text="select..", validators=[DataRequired()])
    subcounty = QuerySelectField('Home Subcounty', get_label="name", allow_blank=True, blank_text="select..", validators=[DataRequired()])
    village = StringField('Village', validators=[DataRequired()])
    chief = StringField('Home chief', validators=[DataRequired()])
    submit = SubmitField('Submit')

    """def __init__(self, *args, **kwargs):
      super(EmployeeHomeAndContactDetailsForm, self).__init__(*args, **kwargs)
      self.region.choices = [(region.id, region.name) for region in Region.query.order_by(Region.name).all()]
      self.county.choices = []

      #self.county.choices =[(county.id, county.name) for county in County.filter_by(County.region_id=1).all()]

    def populate_counties(self):
        region_id = self.region.data
        if region_id:
            counties = County.query.filter_by(region_id=region_id).order_by(County.name).all()
            self.county.choices = [(county.id, county.name) for county in counties]
        else:
            self.county.choices = []"""

class NextOfKinForm(FlaskForm):
   name = StringField('Name', validators=[DataRequired()])
   id_number = IntegerField('Id number', validators=[DataRequired()])
   primary_mobile = IntegerField('Mobile number', validators=[DataRequired()])
   email = EmailField('Email', validators=[Email()])
   gender = QueryRadioField('Gender', query_factory=lambda: Gender.query.all(), get_label="name")
   address = TextAreaField('Address')
   submit = SubmitField('Submit')

class DepedantForm(FlaskForm):
   name = StringField('Name', validators=[DataRequired()])
   id_number = StringField('ID/(Birthcertificate) number ', validators=[DataRequired()])
   primary_mobile = IntegerField('Mobile number', validators=[DataRequired()])
   email = EmailField('Email', validators=[Email()])
   relation_id = SelectField('Relation', coerce=int, validators=[DataRequired()])
   submit = SubmitField('Submit')


class TryForm(FlaskForm):
    primary_mobile = IntegerField('Primary mobile number', validators=[DataRequired()])
    alternate_mobile = IntegerField('Alternate mobile')
    email = EmailField ('Working email', validators=[DataRequired(), Email()])
    postal_address = TextAreaField ('Permanent Address', validators=[DataRequired()])
    region = QuerySelectField('Region', query_factory=lambda: Region.query.all(), allow_blank=True,get_label='name')
    county = QuerySelectField('county', get_label='name', allow_blank=True)
    subcounty = SelectField('Home Subcounty', coerce=int, validators=[DataRequired()])
    village = StringField('Village', validators=[DataRequired()])
    chief = StringField('Home chief', validators=[DataRequired()])

class LocationForm(FlaskForm):
    region = QuerySelectField('Region', query_factory=lambda: Region.query.all(), allow_blank=True, get_label="name")
    county = QuerySelectField('County', get_label="name", allow_blank=True, validators=[DataRequired()])
    
