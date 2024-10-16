from flask import render_template, request
from RECEBIMENTO import db
from flask_login import login_required, current_user
from RECEBIMENTO.models import Responsavel
from sqlalchemy import desc
from . import tabela_bp


@tabela_bp.route('/responsaveis')
@login_required
def tabela_responsaveis():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Consulta para trazer os responsaveis
    responsaveis = db.session.query(Responsavel)\
        .order_by(desc(Responsavel.nome_responsavel))\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/tabela_responsaveis.html', responsaveis=responsaveis, id_responsavel=current_user.id_responsavel)
