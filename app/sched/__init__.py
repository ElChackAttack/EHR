from flask import Blueprint

sched = Blueprint('sched',__name__)

from . import views
