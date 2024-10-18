from flask import render_template, abort, request
from RECEBIMENTO import db
from sqlalchemy import func
from flask_login import login_required
from RECEBIMENTO.models import Filiais, Registro, NotaFiscal
from . import associacoes_bp


@associacoes_bp.route('/registros/atuais/filial/<string:filial>')
@login_required
def tabela_registros_atuais_por_filial(filial):
    try:
        filial_enum = Filiais[filial]  # Tenta obter a filial do Enum
    except KeyError:
        abort(404)  # Se não encontrar, retorna erro 404

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Subconsulta para encontrar o último registro por id_nota_fiscal
    subquery = db.session.query(
        Registro.id_nota_fiscal,
        func.max(Registro.data_criacao).label('max_data_criacao')
    ).group_by(Registro.id_nota_fiscal).subquery()

    # Consulta principal para trazer os registros mais recentes por id_nota_fiscal e filtrar e filial
    registros = db.session.query(Registro)\
        .join(subquery, (Registro.id_nota_fiscal == subquery.c.id_nota_fiscal) & (Registro.data_criacao == subquery.c.max_data_criacao))\
        .join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)\
        .filter(NotaFiscal.filial == filial_enum)\
        .order_by(Registro.data_criacao.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tabelas/associacoes/tabela_registros_atuais_por_filial.html', registros=registros, filial=filial_enum)
