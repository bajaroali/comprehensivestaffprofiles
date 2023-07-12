from flask import render_template, request, redirect, flash, url_for, jsonify
from app.employee import employee
from wtforms.validators import DataRequired, Length, Email, Regexp
from app.models import db, Employee, Region, County, Subcounty, NextOfKin
from .employee_forms import EmployeeBiodataForm, EmployeeHomeAndContactDetailsForm, NextOfKinForm, DepedantForm, TryForm, LocationForm



@employee.route('/addemployee', methods =['GET', 'POST'])
def addemployee():
    form = EmployeeBiodataForm()
    if form.validate_on_submit():
        employee= Employee(service_number= form.service_number.data,
                           pf_number = form.pf_number.data,
                           id_number = form.id_number.data,
                           tax_pin = form.tax_pin.data,
                           gender_id = form.gender.data.id,
                           first_name = form.first_name.data,
                           middle_name = form.middle_name.data,
                           last_name = form.last_name.data,
                           tribe_id = form.tribe.data.id,
                           dob = form.dob.data,
                           blood_group = form.blood_group.data,
                           identification_marks = form.identification_marks.data,
                           height = str(form.height.data),
                           face_shape = form.face_shape.data,
                           transferin_date = form.transferin_date.data,
                           enlistement_date = form.enlistment_date.data,
                           confirmation_date = form.confirmation_date.data,
                           rank_id = form.rank.data,
                           section_id = form.section.data)
        db.session.add(employee)
        db.session.commit()
 
        flash('Biodata saved ', category ='success')
        return redirect(url_for('employee.employeecontactandhomedetails', id=employee.id))
    return render_template ('employee/addemployee.html', form=form)

@employee.route('/employeecontactandhomedetails/<int:id>', methods=['GET', 'POST'])
def employeecontactandhomedetails(id):

    employee = Employee.query.filter_by(id=id).first()
    form = EmployeeHomeAndContactDetailsForm()
    if form.region.data:
        form.county.query = County.query.filter_by(region_id=form.region.data.id).all()
    else:
        form.county.query = County.query.filter(None).all()
    if form.county.data:
        form.subcounty.query= Subcounty.query.filter_by(county_id=form.county.data.id).all()
    else:
        form.subcounty.query = Subcounty.query.filter(None).all()

    if form.validate_on_submit():
        employee.primary_mobile = form.primary_mobile.data
        employee.alternate_mobile = form.alternate_mobile.data
        employee.email = form.email.data
        employee. postal_address = form.postal_address.data
        employee.region_id = form.region.data.id
        employee.county_id = form.county.data.id
        employee.subcounty_id = form.subcounty.data.id
        employee.village = form.village.data
        employee.chief = form.chief.data
         
        db.session.commit()
        flash ('Contact and home details updated successfully', category='success')
        return redirect(url_for('employee.addnextofkin', id=employee.id))
    return render_template('/employee/employeecontactandhomedetails.html',form=form, employee=employee)

@employee.route('/addnextofkin/<int:id>', methods=['GET', 'POST'])
def addnextofkin(id):
    employee = Employee.query.filter_by(id=id).first()
    form = NextOfKinForm()
    if form.validate_on_submit():
        nextofkin = NextOfKin(name = form.name.data,
                              id_number = form.id_number.data,
                              primary_mobile = form.primary_mobile.data,
                              email = form.email.data,
                              gender_id = form.gender.data.id,
                              address = form.address.data,
                              employee_id = employee.id)
        db.session.add(nextofkin)
        db.session.commit()
        flash('Next of kin details succefully added. You may add another employe details.', category='success')
        return redirect (url_for('employee.employeesprofiles'))
    return render_template('employee/addnextofkin.html', form=form, employee=employee)

@employee.route('/employeesprofiles', methods=['GET'])
def employeesprofiles():
    employees =Employee.query.all()
    return render_template ('/employee/employeesprofiles.html', employees=employees)

@employee.route('/get_counties')
def get_counties():
    region_id = request.args.get('region', type=int)
    counties = County.query.filter_by(region_id=region_id).all()
    return render_template('/employee/county_options.html', counties=counties)
    
@employee.route('/employeeprofile/<int:id>', methods=['GET', 'POST'])
def employeeprofile(id):
    employee = Employee.query.filter_by(id=id).first()
    nextofkin = NextOfKin.query.filter_by(employee_id=employee.id).first()
    return render_template('/employee/employeeprofile.html', employee=employee, nextofkin=nextofkin)

@employee.route('/get_subcounties')
def get_subcounties():
    
    county_id = request.args.get('county', type=int)
    subcounties = Subcounty.query.filter_by(county_id=county_id).all()
    return render_template('/employee/subcounty_options.html',subcounties=subcounties)
