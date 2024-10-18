from flask import render_template, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import ResponsavelFilial, Responsavel
from . import associacoes_bp


@associacoes_bp.route('/filiais/responsavel/<int:id_responsavel>')
@login_required
def tabela_filiais_por_responsavel(id_responsavel):
    try:
        responsavel = Responsavel.query.get_or_404(id_responsavel)
    except Exception as e:
        print(f"Erro ao buscar responsável com ID {id_responsavel}: {e}")

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Consulta para trazer as filiais por responsável
    filiais_responsavel = db.session.query(ResponsavelFilial)\
        .filter_by(id_responsavel=responsavel.id_responsavel)\
        .order_by(ResponsavelFilial.id_responsavel)\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/associacoes/tabela_filiais_por_responsavel.html', filiais_responsavel=filiais_responsavel)
