from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField#,DateField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from datetime import datetime, date
from .. import db
from ..models import User, Hospital
from wtforms.widgets.core import html_params
from wtforms.widgets import HTMLString

class InlineButtonWidget(object):
    """
    Render a basic ``<button>`` field.
    """
    input_type = 'submit'
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('value', field.label.text)
        return HTMLString('<button %s> Login' % self.html_params(name=field.name, **kwargs))



class InlineSubmitField(BooleanField):
    """
    Represents an ``<button type="submit">``.  This allows checking if a given
    submit button has been pressed.
    """
    widget = InlineButtonWidget()

class PatientRegistrationForm(FlaskForm):
    
    hospital = SelectField('Hospital', validators = [Required()], coerce = int)
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    first_name = StringField('First Name', validators = [Required(), Length(1, 64), Regexp('^[A-Za-z\s]*$', 0, 'Name must have only letters')])
    last_name = StringField('Last Name', validators = [Required(), Length(1, 64), Regexp('^[A-Za-z\s]*$', 0, 'Name must have only letters')])
    #middle_name = StringField('Middle Name', validators = [Regexp('^[A-Za-z\s]*$', 0, 'Name must have only letters')])
    date_of_birth = DateField('Date of Birth', validators = [Required(), DateRange(date(1900,1,1), date.today())])
    password = PasswordField('Password', validators = [Required(), Length(8,64), EqualTo('password2', message = 'Passwords must match.')])
    password2 = PasswordField('Confirm password', validators = [Required()])
    submit = InlineSubmitField('Register')
    #When a form defines a method with the prefix validate_ followed by the name of a field,
    #the method is invoked in addition to any regularly defined validators
    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators = [Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = InlineSubmitField('Log In')

