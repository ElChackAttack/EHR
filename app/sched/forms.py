from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextField#,DateField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms_components import DateRange
from datetime import datetime, date
from .. import db
from ..models import User

class PatientAppointmentForm(FlaskForm):
    physician = SelectField('Physician', validators = [Required()], coerce=int)
    purpose = StringField('Purpose', validators = [Required()])
    time_slot = DateTimeField('Time Slot', validators = [Required()])
    notes = TextField('Additional Information', validators = [Length(0,500)])
    submit = SubmitField('Book')
