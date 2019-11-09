from flask import Blueprint

roomres = Blueprint('roomres',__name__)

from . import views
