from flask import render_template, abort, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import Filiais, Registro, NotaFiscal
from . import associacoes_bp


@associacoes_bp.route('/registros/filial/<string:filial>')
@login_required
def tabela_todos_registros_por_filial(filial):
    try:
        filial_enum = Filiais[filial]  # Tenta obter a filial do Enum
    except KeyError:
        abort(404)  # Se não encontrar, retorna erro 404

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Consulta para trazer todos os registros por filial
    registros = db.session.query(Registro)\
        .join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)\
        .filter(NotaFiscal.filial == filial_enum)\
        .order_by(Registro.id_registro.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tabelas/associacoes/tabela_todos_registros_por_filial.html', registros=registros, filial=filial_enum)
