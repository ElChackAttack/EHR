from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

#Routes are stored in the views.py module inside the package (main)
#Error handlers are also stored here at errors.py
