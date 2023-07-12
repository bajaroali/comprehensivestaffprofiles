from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from flask_login import UserMixin
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



#create an instance of the extension/ initializing it
db = SQLAlchemy()
login_manager =LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message='This is a protected area.No anonymous access allowed. Please login first.'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    pf_number = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password_enc = db.Column(db.String(256))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    last_active = db.Column(db.DateTime, default= datetime.utcnow())
    is_approved = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>'%self.username
    
    @property
    def password(self):
        raise AttributeError('Warning! Password not readable.')
    @password.setter
    def password(self, password):
        self.password_enc = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_enc, password)

class Role(db.Model):
    __tablename__ ='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index= True)
    users = db.relationship('User', backref='role')

class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True, index=True)
    employees =db.relationship('Employee', backref='section')

class Rank(db.Model):
    __tablename__ = 'ranks'
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    abbreviation =db.Column(db.String(8), unique=True, index=True)
    employees = db.relationship('Employee', backref='rank')

class Designation(db.Model):
    __tablename__ = 'designations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)

class Region(db.Model):
    __tablename__ ='regions'
    id = db.Column( db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    counties =db.relationship('County', back_populates='region')

class County(db.Model):
    __tablename__='counties'
    id =db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(64), unique=True, index=True)
    county_code= db.Column (db.Integer, unique=True, index=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    region = db.relationship('Region', back_populates='counties')
    subcounties = db.relationship('Subcounty', backref='county')
    employees = db.relationship('Employee', backref='county')

class Subcounty(db.Model):
    __tablename__='subcounties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    county_id =db.Column(db.Integer, db.ForeignKey('counties.id'))

class Employee(db.Model):
    __tablename__ ='employees'
    id = db.Column (db.Integer, primary_key=True)
    service_number = db.Column(db.Integer, unique=True, nullable=False, index=True)
    pf_number =db.Column(db.Integer, unique=True, nullable=False, index=True)
    id_number = db.Column(db.Integer, unique = True, nullable=False, index=True)
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))
    dob = db.Column(db.DateTime)
    tax_pin = db.Column(db.String(30), unique = True, nullable=False, index=True)
    first_name =db.Column(db.String(30))
    middle_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(64), unique=True, index=True)
    primary_mobile = db.Column(db.Integer, unique=True)
    alternate_mobile = db.Column(db.Integer, unique=True, nullable=True)
    postal_address = db.Column(db.String(128))
    transferin_date = db.Column (db.DateTime)
    enlistement_date =db.Column(db.DateTime)
    confirmation_date = db.Column( db.DateTime)
    rank_id =db.Column(db.Integer, db.ForeignKey('ranks.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    county_id = db.Column(db.Integer, db.ForeignKey('counties.id'))
    subcounty_id = db.Column(db.Integer, db.ForeignKey('subcounties.id'))
    blood_group = db.Column(db.String(16), index=True)
    identification_marks= db.Column(db.String(128))
    height = db.Column(db.String)
    face_shape = db.Column(db.String())
    chief = db.Column (db.String(64))
    village = db.Column(db.String(64))
    tribe_id = db.Column(db.Integer, db.ForeignKey('tribes.id'))

class Gender(db.Model):
    __tablename__ ='genders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column (db.String(64), unique=True)
    employees = db.relationship('Employee', backref='gender')
    nextofkins = db.relationship('NextOfKin', backref='gender')



class Depandant(db.Model):
    __tablename__ = 'dependants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    id_number = db.Column(db.Integer, unique=True)
    primary_mobile = db.Column(db.Integer(), unique=True)
    email = db.Column(db.String(64))
    relation_id = db.Column(db.Integer, db.ForeignKey('relations.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

class Relation(db.Model):
    __tablename__ ='relations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

class Tribe(db.Model):
    __tablename__ ='tribes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    employees = db.relationship('Employee', backref='tribe')


class NextOfKin(db.Model):
    __tablename__= 'nextofkins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    id_number = db.Column(db.Integer, unique=True)
    primary_mobile = db.Column(db.Integer(), unique=True)
    email = db.Column(db.String(64))
    address = db.Column(db.String(128))
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

class Deployment(db.Model):
    __tablename__='deployments'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column (db.Integer, db.ForeignKey('employees.id'))
    section_id = db.Column (db.Integer, db.ForeignKey('sections.id'))
    deployment_date = db.Column(db.DateTime, default=datetime.utcnow())
    end_date = db.Column(db.DateTime)
    employee = db.relationship(Employee)
    section = db.relationship(Section)


class LeaveApplication(db.Model):
    __tablename__ = 'leave_applications'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    reason = db.Column(db.String)
    status = db.Column(Enum('pending', 'approved', 'rejected'), default='pending')
    employee = db.relationship(Employee)

class LeaveApproval(db.Model):
    __tablename__ = 'leave_approvals'

    id = db.Column(db.Integer, primary_key=True)
    leave_application_id = db.Column(db.Integer, db.ForeignKey('leave_applications.id'))
    approver_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    comment = db.Column(db.String(256))
    status = db.Column(Enum('approved', 'rejected'))
    leave_application = db.relationship(LeaveApplication)
    approver = db.relationship(Employee)


    """id (Primary Key), full_name, mobile,
      postal_address, employee_id (Foreign Key to Employee Table),
        relation_id, phone_number, email"""




