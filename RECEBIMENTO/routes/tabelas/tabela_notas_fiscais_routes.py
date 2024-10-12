from flask import render_template, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import NotaFiscal
from sqlalchemy import desc
from . import tabela_bp


@tabela_bp.route('/notas_fiscais')
@login_required
def tabela_notas_fiscais():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Consulta para trazer as notas fiscais
    notas_fiscais = db.session.query(NotaFiscal)\
        .order_by(desc(NotaFiscal.data_alteracao))\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/tabela_notas_fiscais.html', notas_fiscais=notas_fiscais)
