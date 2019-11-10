from flask import render_template, redirect, request, url_for, flash
from . import sched
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Patient, User, Physician_schedule, Physician
from .. import db
from .forms import PatientAppointmentForm
import re


@sched.route('/schedule', methods = ['GET','POST'])
@login_required
def schedule():
    form = PatientAppointmentForm()
    physicians = Physician.query.join(User).filter_by(hospital_id=current_user.hospital_id).all()
    physician_users = User.query.filter(User.user_id.in_([ret.user_id for ret in physicians])).all()
    form.physician.choices = [(ret.user_id, "Dr. {} {}".format(ret.first_name,ret.last_name) ) for ret in physician_users]
    physician_schedule = Physician_schedule.query.filter(Physician_schedule.physician_id.in_([ret.user_id for ret in physicians])).all()
    # print([(ret.user_id, "Dr.{} {}".format(ret.first_name,ret.last_name) ) for ret in physician_users])
    #render the schedule table from the physician table, with physician set to the
    #last visited physician, else alphabetical

    return render_template('sched/schedule.html', form = form, physician_schedule = physician_schedule)

