from flask import render_template, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import ResponsavelFilial
from . import tabela_bp


@tabela_bp.route('/responsaveis_filial')
@login_required
def tabela_responsaveis_filial():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Consulta para trazer os responsaveis, ordenando pelo nome da filial
    responsaveis_filial = db.session.query(ResponsavelFilial)\
        .order_by(ResponsavelFilial.filial)\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/tabela_responsaveis_filial.html', responsaveis_filial=responsaveis_filial)
