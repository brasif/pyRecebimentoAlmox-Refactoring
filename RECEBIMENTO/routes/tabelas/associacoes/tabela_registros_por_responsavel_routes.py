from flask import render_template, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import Responsavel, Registro
from . import associacoes_bp


@associacoes_bp.route('/registros/responsavel/<int:id_responsavel>')
@login_required
def tabela_registros_por_responsavel(id_responsavel):
    responsavel = Responsavel.query.get_or_404(id_responsavel)

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Consulta para trazer todos os registros vinculados ao id_responsavel
    registros = db.session.query(Registro)\
        .filter_by(id_responsavel=responsavel.id_responsavel)\
        .order_by(Registro.data_criacao.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/associacoes/tabela_registros_por_responsavel.html', registros=registros, id_responsavel=responsavel.id_responsavel)
