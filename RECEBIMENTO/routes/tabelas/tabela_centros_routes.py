from flask import render_template, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import Centro
from sqlalchemy import desc
from . import tabela_bp


@tabela_bp.route('/centros')
@login_required
def tabela_centros():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Consulta para trazer os centros
    centros = db.session.query(Centro)\
        .order_by(desc(Centro.data_alteracao))\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tabelas/tabela_centros.html', centros=centros)
