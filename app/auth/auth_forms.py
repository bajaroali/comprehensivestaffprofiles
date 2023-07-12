from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, EmailField, FileField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Role, User, Section, Rank, Region, County, Subcounty

class LoginForm(FlaskForm):
    email = EmailField('Email address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    login = SubmitField('Login')

class RegistrationForm(FlaskForm):
    pf_number = StringField('PF number', validators=
                            [DataRequired(message='This is a required field'),
                              Length(min=10, message='It should have a minimum of 10 digits'),
                              
                                                     ])
    user_name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.'), Length(min=7)])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    approved = BooleanField(('Approved/Confirmed'))
    role = QuerySelectField('Role', query_factory=lambda: Role.query.all(), get_label="name", allow_blank=True, validators=[DataRequired()])
    register = SubmitField('Register')

    #Replaced with QuerySelectField
    """def __init__(self, *args, **kwargs):
      super(RegistrationForm, self).__init__(*args, **kwargs)
      self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]"""
   
    def validate_email(self, field):
      if  User.query.filter_by(email=field.data).first():
         raise ValidationError('Email already registered.')
      
    def validate_pf_number(self, field):
      if  User.query.filter_by(pf_number=field.data).first():
         raise ValidationError('The PF number provided has already been used.')

class UserEditForm(FlaskForm):
    image = FileField('Upload user image:', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    pf_number = StringField('PF number', validators=
                            [DataRequired(message='This is a required field'),
                              Length(min=10, message='It should have a minimum of 10 digits'),
                              
                                                     ])
    user_name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(),Email()])
    
    approved = BooleanField(('Approved/Confirmed'))
    role = SelectField('Role', coerce=int)
    register = SubmitField('Update')

    def __init__(self, *args, **kwargs):
      super(UserEditForm, self).__init__(*args, **kwargs)
      self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
   

      
class AddRoleForm(FlaskForm):
   name = StringField('System Role', validators=[DataRequired(), Length(min=5)])
   add = SubmitField('Add')

   def validate_name(self, field):
      if Role.query.filter_by(name= field.data).first():
         raise ValidationError('That role is already defined in the system.')

class EditRoleForm(FlaskForm):
   name = StringField('System Role', validators=[DataRequired(), Length(min=5)])
   add = SubmitField('Update')

   def validate_name(self, field):
      if Role.query.filter_by(name= (field.data).strip()).first():
         raise ValidationError('That role already exists.')

class AddSectionForm(FlaskForm):
   name = StringField('Section name', validators=[DataRequired(), Length(min=3)])
   add = SubmitField('Add')

   def validate_name(self, field):
      if Section.query.filter_by(name= field.data).first():
         raise ValidationError('The section already exists in the system.')

class EditSectionForm(FlaskForm):
   name = StringField('Section name', validators=[DataRequired(), Length(min=3)])
   add = SubmitField('Add')

   def validate_name(self, field):
      if Section.query.filter_by(name= field.data).first():
         raise ValidationError('The section already exists in the system.')
    
class AddRankForm(FlaskForm):
   name = StringField('Name of Rank', validators=[DataRequired()])
   abbreviation = StringField('Abbreviation', validators=[DataRequired()])
   add = SubmitField('Add')

   def validate_name(self, field):
      if Rank.query.filter_by(name= field.data).first():
         raise ValidationError('That rank already exists in the system.')
   
   def validate_abbreviation(self, field):
      if Rank.query.filter_by(abbreviation= field.data).first():
         raise ValidationError('That abbreviation has been used.')

class EditRankForm(FlaskForm):
   name = StringField('Name of Rank', validators=[DataRequired()])
   abbreviation = StringField('Abbreviation', validators=[DataRequired()])
   add = SubmitField('Update')

   def validate_name(self, field):
      if Rank.query.filter_by(name= (field.data).strip()).first():
         raise ValidationError('That rank already exists.')
      
   def validate_abbreviation(self, field):
      if Rank.query.filter_by(abbreviation= (field.data).strip()).first():
         raise ValidationError('That abbreviationhas been used.')

#Regions, counties, subcounties forms

class AddRegionForm(FlaskForm):
   name = StringField('Region name', validators=[DataRequired(), Length(min=3)])
   add = SubmitField('Add')

   def validate_name(self, field):
      if Region.query.filter_by(name= field.data).first():
         raise ValidationError('The region already exists in the system.')

class EditRegionForm(FlaskForm):
   name = StringField('Region name', validators=[DataRequired(), Length(min=3)])
   add = SubmitField('Update')

   def validate_name(self, field):
      if Region.query.filter_by(name= field.data).first():
         raise ValidationError('The region already exists in the system.')

class AddCountyForm(FlaskForm):
   name = StringField('County name', validators=[DataRequired(), Length(min=3)])
   county_code = StringField('County Code', validators=[DataRequired(), Length(min=3, max=3)])
   region_id = QuerySelectField('Region', query_factory=lambda:Region.query.all(), get_label="name", allow_blank=True,validators=[DataRequired()])
   add = SubmitField('Add')

   def validate_name(self, field):
      if County.query.filter_by(name= field.data).first():
         raise ValidationError('The county already exists in the system.')
   
   def validate_county_code(self, field):
      if County.query.filter_by(county_code= field.data).first():
         raise ValidationError('The couunty code has been used alreadyin the system.')
      
class EditCountyForm(FlaskForm):
   name = StringField('County name', validators=[DataRequired(), Length(min=3)])
   county_code = StringField('County Code', validators=[DataRequired(), Length(min=3, max=3)])
   region_id = SelectField('Region', coerce=int)
   add = SubmitField('Update')

   def __init__(self, *args, **kwargs):
      super(EditCountyForm, self).__init__(*args, **kwargs)
      self.region_id.choices = [(region.id, region.name) for region in Region.query.order_by(Region.name).all()]
      

   """def validate_name(self, field):
      if County.query.filter_by(name= field.data).first():
         raise ValidationError('The county already exists in the system.')
   
   def validate_county_code(self, field):
      if County.query.filter_by(county_code= field.data).first():
         raise ValidationError('The couunty code has been used alreadyin the system.')"""
      
#Subcounty forms
class AddSubcountyForm(FlaskForm):
   name = StringField('Sub county name', validators=[DataRequired(), Length(min=3)])
   county_id = SelectField('County', coerce=int)
   add = SubmitField('Add')

   def __init__(self, *args, **kwargs):
      super(AddSubcountyForm, self).__init__(*args, **kwargs)
      self.county_id.choices = [(county.id, county.name) for county in County.query.order_by(County.name).all()]
      

   def validate_name(self, field):
      if Subcounty.query.filter_by(name= field.data).first():
         raise ValidationError('The subcounty already exists in the system.')
      
class EditSubcountyForm(FlaskForm):
   name = StringField('County name', validators=[DataRequired(), Length(min=3)])
   county_id = SelectField('County', coerce=int)
   add = SubmitField('Update')

   def __init__(self, *args, **kwargs):
      super(EditSubcountyForm, self).__init__(*args, **kwargs)
      self.county_id.choices = [(county.id, county.name) for county in County.query.order_by(County.name).all()]
      

   def validate_name(self, field):
      if County.query.filter_by(name= field.data).first():
         raise ValidationError('The subcounty already exists in the system.')
      