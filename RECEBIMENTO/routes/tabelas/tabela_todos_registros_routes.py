from flask import render_template, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import Registro
from sqlalchemy import desc
from . import tabela_bp


@tabela_bp.route('/registros')
@login_required
def tabela_todos_registros():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Consulta para trazer todos os registros
    registros = db.session.query(Registro)\
        .order_by(desc(Registro.id_registro))\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/tabela_todos_registros.html', registros=registros)
