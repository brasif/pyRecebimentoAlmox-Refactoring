from flask import render_template, request
from RECEBIMENTO import db
from sqlalchemy import func
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

    # Subconsulta para encontrar o último registro por id_nota_fiscal
    subquery = db.session.query(
        Registro.id_nota_fiscal,
        func.max(Registro.data_criacao).label('max_data_criacao')
    ).group_by(Registro.id_nota_fiscal).subquery()

    # Consulta principal para trazer os registros mais recentes por id_nota_fiscal
    registros = db.session.query(Registro)\
        .join(subquery, (Registro.id_nota_fiscal == subquery.c.id_nota_fiscal) & (Registro.data_criacao == subquery.c.max_data_criacao))\
        .filter(Registro.id_responsavel == id_responsavel)\
        .order_by(Registro.data_criacao.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tabelas/associacoes/tabela_registros_por_responsavel.html', registros=registros, id_responsavel=responsavel.id_responsavel)
