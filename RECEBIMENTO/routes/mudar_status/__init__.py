from flask import Blueprint

mudar_status_bp = Blueprint('mudar_status', __name__, url_prefix="/mudar_status")


from .mudar_status_routes import *