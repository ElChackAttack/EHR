from flask import render_template, redirect, request, url_for, flash
from . import sched
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Patient, User
from .. import db
import re


@sched.route('/schedule', methods = ['GET','POST'])
def schedule():
    return render_template("/sched/schedule.html")

