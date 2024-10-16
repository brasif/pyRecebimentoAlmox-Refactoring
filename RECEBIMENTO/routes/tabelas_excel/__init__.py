from flask import Blueprint

tabelas_excel_bp = Blueprint('tabelas_excel', __name__, url_prefix="/tabelas_excel")


from .excel_notas_fiscais_routes import *
from .excel_responsaveis_routes import *
from .excel_todos_registros_routes import *
from .excel_ultimos_registros_routes import *