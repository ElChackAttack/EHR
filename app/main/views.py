from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from ..auth.forms import LoginForm

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..models import User

@main.route('/', methods = ['GET','POST'])
def index():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user is not None and user.verify_password(loginform.password.data):
            login_user(user, loginform.remember_me.data)
            #if login form was presented to the user to prevent
            #unauthorized access to a protected URL, Flask-Login
            #Saves the original URL in the next query string
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid email or password.')
    return render_template('index.html', login_form = loginform)

def home():
    return render_template('home.html')
