from flask import Blueprint

inscripciones_bp = Blueprint('inscripciones', __name__)

from . import routes
