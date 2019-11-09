from flask import render_template, redirect, request, url_for, flash
from . import roomres
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Patient, User, Physician
from .. import db
import re

@roomres.route('/reserve', methods = ['GET','POST'])
def reserve():
    full_rooms = [i for i in range(0,1000,2)]
    all_rooms = [i for i in range(0,1000)]
    return render_template("/roombooking/room_booking.html", full_rooms = full_rooms, all_rooms = all_rooms)
#Here comes the scheduling code...

#Here comes the scheduling code...
