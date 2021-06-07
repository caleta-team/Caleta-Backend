from flask import Blueprint
API_bp = Blueprint('api', __name__, template_folder='templates')
from . import routes