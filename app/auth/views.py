from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Patient, User, Hospital
from .forms import LoginForm, PatientRegistrationForm
from ..email import send_email
from .. import db
import re


@auth.route('/login', methods = ['GET','POST'])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            #if login form was presented to the user to prevent
            #unauthorized access to a protected URL, Flask-Login
            #Saves the original URL in the next query string
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid email or password.')
        #if the username or password is incorrect, form is
        #rendered again
    return render_template('auth/login.html', login_form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

"""

This registration is unique for patients since the roles of nurse and physician have senitive
privileges which we don't want just anyone interacting with the platform to be able to
register.

"""

@auth.route('/register', methods = ['GET', 'POST'])
def register_patient():
    hospitals = Hospital.query.all()
    form = PatientRegistrationForm()
    form.hospital.choices = [(h.unique_id, h.name) for h in hospitals]
    print(form.hospital.choices)
    if form.validate_on_submit():
        print(form.hospital.data)
        user = User(email = form.email.data,
                    password = form.password.data,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    hospital_id = form.hospital.data)
        db.session.add(user)
        print(user)
        db.session.commit()
        print(user)
        patient = Patient(date_of_birth = form.date_of_birth.data, user = user)
        db.session.add(patient)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                     'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_patient.html', form = form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


#The current_user variables used in the conditional is
#defined by Flask-Login and is automatically available
#to view functions and templates
