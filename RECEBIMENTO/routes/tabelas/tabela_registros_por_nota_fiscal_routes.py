from flask import render_template, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import NotaFiscal, Registro
from . import tabela_bp


@tabela_bp.route('/registros/nota_fiscal/<int:id_nota_fiscal>')
@login_required
def registros_por_nota_fiscal(id_nota_fiscal):
    nota_fiscal = NotaFiscal.query.get_or_404(id_nota_fiscal)

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Consulta para trazer todos os registros vinculados ao id_nota_fiscal
    registros = db.session.query(Registro)\
        .filter_by(id_nota_fiscal=nota_fiscal.id_nota_fiscal)\
        .order_by(Registro.data_criacao.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/registros_por_nota_fiscal.html', registros=registros, id_nota_fiscal=nota_fiscal.id_nota_fiscal)
