from flask import render_template, redirect, url_for, request, flash
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import NotaFiscal, Registro
from . import associacoes_bp


@associacoes_bp.route('/registros/nota_fiscal/<int:id_nota_fiscal>')
@login_required
def tabela_todos_registros_por_nota_fiscal(id_nota_fiscal):

    try:
        # Verifica se o id da nota fiscal passado como parâmetro existe no banco de dados
        nota_fiscal = NotaFiscal.query.get_or_404(id_nota_fiscal)

        # Paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        
        # Consulta para trazer todos os registros vinculados ao id_nota_fiscal, ordenados pelo id do registro
        registros = db.session.query(Registro)\
            .filter_by(id_nota_fiscal=nota_fiscal.id_nota_fiscal)\
            .order_by(Registro.id_registro.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return render_template('/tabelas/associacoes/tabela_todos_registros_por_nota_fiscal.html', registros=registros, id_nota_fiscal=nota_fiscal.id_nota_fiscal)

    except:
        # Exibe um erro específico no flash com detalhes
        flash("Ocorreu um erro ao carregar os registros por nota fiscal. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))