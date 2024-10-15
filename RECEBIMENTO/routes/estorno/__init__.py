from flask import Blueprint

estorno_bp = Blueprint('estorno', __name__, url_prefix="/estorno")


from .estorno_routes import *