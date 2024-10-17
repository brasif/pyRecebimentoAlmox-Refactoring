from flask import render_template, abort, request
from RECEBIMENTO import db
from flask_login import login_required, current_user
from RECEBIMENTO.models import ResponsavelFilial, Filiais
from sqlalchemy import desc
from . import associacoes_bp


@associacoes_bp.route('/responsaveis/filial/<string:filial>')
@login_required
def tabela_responsaveis_por_filial(filial):
    try:
        filial_enum = Filiais[filial]  # Tenta obter a filial do Enum
    except KeyError:
        abort(404)  # Se não encontrar, retorna erro 404

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Consulta para trazer os responsaveis por filial
    responsaveis = db.session.query(ResponsavelFilial)\
        .filter_by(filial=filial_enum)\
        .order_by(ResponsavelFilial.id_responsavel)\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/associacoes/tabela_responsaveis_por_filial.html', responsaveis=responsaveis, filial=filial_enum, id_responsavel=current_user.id_responsavel)
