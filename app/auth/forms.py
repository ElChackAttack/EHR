from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField#,DateField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from datetime import datetime, date
from .. import db
from ..models import User

class PatientRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    first_name = StringField('First Name', validators = [Required(), Length(1, 64), Regexp('^[A-Za-z\s]*$', 0, 'Name must have only letters')])
    last_name = StringField('Last Name', validators = [Required(), Length(1, 64), Regexp('^[A-Za-z\s]*$', 0, 'Name must have only letters')])
    #middle_name = StringField('Middle Name', validators = [Regexp('^[A-Za-z\s]*$', 0, 'Name must have only letters')])
    date_of_birth = DateField('Date of Birth', validators = [Required(), DateRange(date(1900,1,1), date.today())])
    password = PasswordField('Password', validators = [Required(), Length(8,64), EqualTo('password2', message = 'Passwords must match.')])
    password2 = PasswordField('Confirm password', validators = [Required()])
    submit = SubmitField('Register')
    #When a form defines a method with the prefix validate_ followed by the name of a field,
    #the method is invoked in addition to any regularly defined validators
    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators = [Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
