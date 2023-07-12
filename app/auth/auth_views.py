from app.auth import auth
from flask import render_template, flash, redirect, abort, url_for, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.auth_forms import LoginForm, RegistrationForm, AddRoleForm, EditRoleForm, AddSectionForm, AddRankForm, EditRankForm, UserEditForm, EditSectionForm, AddRegionForm, EditRegionForm, AddCountyForm, EditCountyForm, AddSubcountyForm, EditSubcountyForm
from datetime import datetime
from app.models import db, User, Role, Section, Rank, Region, County, Subcounty,Employee

@auth.route ('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash('You are already signed in. Welcome back.', category='success')
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next=url_for('main.index')
                flash ('Logged in successfully.', category='success')
            return redirect(next)
        flash('Invalid username or password.', category='warning')
    return render_template('auth/login.html', form=form)

@auth.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    form = RegistrationForm()
    if form.validate_on_submit():
        role= Role.query.filter_by(name=form.role.data.id).first()
        user = User(username=form.user_name.data, pf_number=form.pf_number.data, email =form.email.data,
                    password=form.password.data, is_approved=form.approved.data,
                    role_id=form.role.data.id)
        db.session.add(user)
        db.session.commit()
        flash('User account succesfully created.', category='success')
        return redirect(url_for('auth.viewusers'))
    return render_template('auth/register.html', form=form)

@auth.route('/deleteuser/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', category='success')
    return redirect(url_for('auth.viewusers'))

@auth.route('/edituser/<int:id>', methods=['GET', 'POST'])
@login_required
def edituser(id):
    user = User.query.filter_by(id=id).first()
    form = UserEditForm()
    if form.validate_on_submit():
        user.username = form.user_name.data
        user.pf_number = form.pf_number.data
        user.email = form.email.data
        user.approved = form.approved.data
        user.role_id=form.role.data
        db.session.add(user)
        db.session.commit()
        flash('User details updated successfully.', category='success')
        return redirect(url_for('auth.viewuser', id=user.id))
    form.user_name.data = user.username 
    form.pf_number.data = user.pf_number
    form.email.data = user.email
    form.approved.data =  user.is_approved
    form.role.data = user.role_id
    return render_template('auth/edituser.html', user=user, form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/addrole', methods=['GET', 'POST'])
@login_required
def addrole():
    form = AddRoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data)
        db.session.add(role)
        db.session.commit()
        flash('System role succesfully created.', category='success')
        return redirect(url_for('auth.viewroles'))
    return render_template ('auth/addrole.html', form=form)

@auth.route('/viewroles', methods=['GET'])
@login_required
def viewroles():
    roles= Role.query.all()
    return render_template('auth/viewroles.html', roles=roles)

@auth.route('/editrole/<int:id>', methods=['GET', 'POST'])
@login_required
def editrole(id):
    role = Role.query.filter_by(id=id).first()
    form = EditRoleForm()
    if form.validate_on_submit():
        role.name = form.name.data
        db.session.add(role)
        db.session.commit()
        flash('Role edited successfully.', category='success')
        return redirect(url_for('auth.viewroles'))
    form.name.data = role.name
    return render_template('auth/editrole.html', form=form)
    
@auth.route('/deleterole/<int:id>', methods=['GET', 'POST'])
def delete_role(id):
    role = Role.query.get(id)
    if role is None:
        abort(404)
    if User.query.filter_by(role_id=role.id).first():
        flash('Role < %r > cannot be deleted because it is associated with users.Redefine the users first.'%format(role.name), category='danger')
        return redirect(url_for('auth.viewroles'))
    #otherwise delete the row    
    db.session.delete(role)
    db.session.commit()
    flash('Role deleted', category='success')
    return redirect(url_for('auth.viewroles'))

@auth.route('/viewuser/<int:id>', methods=['GET'])
@login_required
def viewuser(id):
    user= User.query.filter_by(id=id).first()
    role= Role.query.filter_by(id=user.role_id).first()
    return render_template('auth/viewuser.html', user=user, role=role)

@auth.route('/viewusers', methods=['GET'])
@login_required
def viewusers():
    users= User.query.all()
    return render_template('auth/viewusers.html', users=users)

@auth.route('/addsection', methods=['GET', 'POST'])
@login_required
def addsection():
    form = AddSectionForm()
    if form.validate_on_submit():
        section = Section(name=form.name.data)
        db.session.add(section)
        db.session.commit()
        flash('Section succesfully created.', category='success')
        return redirect(url_for('auth.viewsections'))
    return render_template ('auth/addsection.html', form=form)

@auth.route('/editsection/<int:id>', methods=['GET', 'POST'])
@login_required
def editsection(id):
    section = Section.query.filter_by(id=id).first()
    form = EditSectionForm()
    if form.validate_on_submit():
        section.name = form.name.data
        db.session.add(section)
        db.session.commit()
        flash('Section details updatedsuccessfully.', category='success')
        return redirect(url_for('auth.viewsection'))
    form.name.data = section.name
    return render_template('auth/editsection.html', form=form)

@auth.route('/viewsections', methods=['GET'])
@login_required
def viewsections():
    sections= Section.query.all()
    return render_template('auth/viewsections.html', sections=sections)

@auth.route('/deletesection/<int:id>', methods=['GET', 'POST'])
def delete_section(id):
    section = Section.query.get(id)
    if section is None:
        abort(404)
    #otherwise delete
    db.session.delete(section)
    db.session.commit()
    flash('Section deleted successfully.', category='success')
    return redirect(url_for('auth.viewsections'))

@auth.route('/addrank', methods=['GET', 'POST'])
@login_required
def addrank():
    form = AddRankForm()
    if form.validate_on_submit():
        rank = Rank(name=form.name.data, abbreviation= form.abbreviation.data)
        db.session.add(rank)
        db.session.commit()
        flash('Rank succesfully created.', category='success')
        return redirect(url_for('auth.viewranks'))
    return render_template ('auth/addrank.html', form=form)

@auth.route('/editrank/<int:id>', methods=['GET', 'POST'])
@login_required
def editrank(id):
    rank = Rank.query.filter_by(id=id).first()
    form = EditRankForm()
    if form.validate_on_submit():
        rank.name = form.name.data
        rank.abbreviation=form.abbreviation.data
        db.session.add(rank)
        db.session.commit()
        flash('Rank updated successfully.', category='success')
        return redirect(url_for('auth.viewranks'))
    form.name.data = rank.name
    form.abbreviation.data = rank.abbreviation
    return render_template('auth/editrole.html', form=form)

@auth.route('/deleterank/<int:id>', methods=['GET', 'POST'])
def delete_rank(id):
    rank = Rank.query.get(id)
    if rank is None:
        abort(404)
    if Employee.query.filter_by(rank_id=rank.id).first():
        flash('Rank < %r > cannot be deleted because it is associated with Officers.Please re-assign them before deleting this role.'%format(rank.name), category='danger')
        return redirect(url_for('auth.viewranks'))
    #otherwise delete the rank row    
    db.session.delete(rank)
    db.session.commit()
    flash('Role deleted', category='success')
    return redirect(url_for('auth.viewranks'))

@auth.route('/viewranks', methods=['GET'])
@login_required
def viewranks():
    ranks= Rank.query.all()
    return render_template('auth/viewranks.html', ranks=ranks)

@auth.route('/addregion', methods=['GET', 'POST'])
@login_required
def addregion():
    form = AddRegionForm()
    if form.validate_on_submit():
        region = Region(name=form.name.data)
        db.session.add(region)
        db.session.commit()
        flash('Region succesfully created.', category='success')
        return redirect(url_for('auth.viewregions'))
    return render_template ('auth/addregion.html', form=form)

@auth.route('/editregion/<int:id>', methods=['GET', 'POST'])
@login_required
def editregion(id):
    region = Region.query.filter_by(id=id).first()
    form = EditRegionForm()
    if form.validate_on_submit():
        region.name = form.name.data
        
        db.session.add(region)
        db.session.commit()
        flash('Region updated successfully.', category='success')
        return redirect(url_for('auth.viewregions'))
    form.name.data = region.name
    return render_template('auth/editregion.html', form=form)

@auth.route('/deleteregion/<int:id>', methods=['GET', 'POST'])
def delete_region(id):
    region = Region.query.get(id)
    if region is None:
        abort(404)
    if County.query.filter_by(region_id=region.id).first():
        flash('Region < %r > cannot be deleted because it is has counties assigned to it .'%format(region.name), category='danger')
        return redirect(url_for('auth.viewregions'))
    #otherwise delete the rank row    
    db.session.delete(region)
    db.session.commit()
    flash('Region deleted succefully.', category='success')
    return redirect(url_for('auth.viewregions'))

@auth.route('/viewregions', methods=['GET'])
@login_required
def viewregions():
    regions= Region.query.order_by(Region.name).all()
    return render_template('auth/viewregions.html', regions=regions)

@auth.route('/addcounty', methods=['GET', 'POST'])
@login_required
def addcounty():
    form = AddCountyForm()
    if form.validate_on_submit():
        county = County(name=form.name.data, county_code=form.county_code.data, region_id=form.region_id.data.id)
        db.session.add(county)
        db.session.commit()
        flash('County succesfully created.', category='success')
        return redirect(url_for('auth.viewcounties'))
    return render_template ('auth/addcounty.html', form=form)

@auth.route('/viewcounties', methods=['GET'])
@login_required
def viewcounties():
    counties= County.query.order_by(County.region_id, County.county_code).all()
    return render_template('auth/viewcounties.html', counties=counties)

@auth.route('/editcounty/<int:id>', methods=['GET', 'POST'])
@login_required
def editcounty(id):
    county = County.query.filter_by(id=id).first()
    form = EditCountyForm()
    if form.validate_on_submit():
        county.county_code=form.county_code.data
        county.name = form.name.data
        county.region_id=form.region_id.data
        
        db.session.add(county)
        db.session.commit()
        flash('County details updated successfully.', category='success')
        return redirect(url_for('auth.viewcounties'))
    form.name.data = county.name
    form.county_code.data = county.county_code
    form.region_id.data = county.region_id
    return render_template('auth/editcounty.html', form=form)

@auth.route('/deletecounty/<int:id>', methods=['GET', 'POST'])
def delete_county(id):
    county = County.query.get(id)
    if county is None:
        abort(404)
    if Subcounty.query.filter_by(county_id=county.id).first():
        flash('County < %r > cannot be deleted because it is has subcounties assigned to it .'%format(county.name), category='danger')
        return redirect(url_for('auth.viewcounties'))
    #otherwise delete the county here    
    db.session.delete(county)
    db.session.commit()
    flash('County deleted succefully.', category='success')
    return redirect(url_for('auth.viewcounties'))

# Subcounty Routes
@auth.route('/addsubcounty', methods=['GET', 'POST'])
@login_required
def addsubcounty():
    form = AddSubcountyForm()
    if form.validate_on_submit():
        subcounty = Subcounty(name=form.name.data, county_id=form.county_id.data)
        db.session.add(subcounty)
        db.session.commit()
        flash('Subcounty succesfully created.', category='success')
        return redirect(url_for('auth.viewsubcounties'))
    return render_template ('auth/addsubcounty.html', form=form)

@auth.route('/viewsubcounties', methods=['GET'])
@login_required
def viewsubcounties():
    subcounties= Subcounty.query.order_by(Subcounty.county_id).all()
    return render_template('auth/viewsubcounties.html', subcounties=subcounties)

@auth.route('/editsubcounty/<int:id>', methods=['GET', 'POST'])
@login_required
def editsubcounty(id):
    subcounty = Subcounty.query.filter_by(id=id).first()
    form = EditSubcountyForm()
    if form.validate_on_submit():
        subcounty.name = form.name.data
        subcounty.county_id = form.county_id.data
        
        db.session.add(subcounty)
        db.session.commit()
        flash('Subcounty details updated successfully.', category='success')
        return redirect(url_for('auth.viewsubcounties'))
    form.name.data = subcounty.name
    form.county_id.data = subcounty.county_id
    return render_template('auth/editsubcounty.html', form=form)

@auth.route('/deletesubcounty/<int:id>', methods=['GET', 'POST'])
def delete_subcounty(id):
    subcounty = Subcounty.query.get(id)
    if subcounty is None:
        abort(404)
    #otherwise delete the county here    
    db.session.delete(subcounty)
    db.session.commit()
    flash('County deleted succefully.', category='success')
    return redirect(url_for('auth.viewsubcounties'))

@auth.route('/viewregionalsettings', methods=["GET", "POST"])
def viewregionalsettings():
    return render_template('auth/viewregionalsettings.html')

#just a test route
@auth.route('/register', methods=["GET", "POST"])
def register1():
    #name = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name= form.user_name.data).first()
        if user is None:
            user = User(user_name=form.user_name.data,
                        email= form.email.data,
                        password_enc =form.password.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            flash('User added successfully.')
        else:
            session['known'] =True
            session['name'] = form.user_name.data
            form.user_name.data = ''
            flash('User already exists.')
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', 
                           form=form, 
                           current_time=datetime.utcnow(), 
                           name=session.get('name'))
            
"""        # name = form.user_name.data
        old_name = session.get('name')
        if old_name is not None and old_name != form.user_name.data:
             flash('Looks like you have changed your name.')
        session['name'] = form.user_name.data
        form.user_name.data = ''
        
        redirect(url_for('auth.register'))
    return render_template('auth/register.html',
                            form = form, name = session.get('name'),
                              current_time = datetime.utcnow())
    #return render_template('auth/login.html', form=form) """