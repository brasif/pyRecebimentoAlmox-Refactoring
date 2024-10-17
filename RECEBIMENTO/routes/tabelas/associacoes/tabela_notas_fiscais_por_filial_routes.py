from flask import render_template, abort, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import NotaFiscal, Filiais
from sqlalchemy import desc
from . import associacoes_bp


@associacoes_bp.route('/notas_fiscais/filial/<string:filial>')
@login_required
def tabela_notas_fiscais_por_filial(filial):
    try:
        filial_enum = Filiais[filial]  # Tenta obter a filial do Enum
    except KeyError:
        abort(404)  # Se não encontrar, retorna erro 404

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Consulta para trazer as notas fiscais por filial
    notas_fiscais = db.session.query(NotaFiscal)\
        .filter_by(filial=filial_enum)\
        .order_by(desc(NotaFiscal.data_alteracao))\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/associacoes/tabela_notas_fiscais_por_filial.html', notas_fiscais=notas_fiscais, filial=filial_enum)
