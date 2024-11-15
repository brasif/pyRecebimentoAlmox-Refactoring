from flask import render_template, redirect, url_for, request, flash
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import ResponsavelFilial, Responsavel
from . import associacoes_bp


@associacoes_bp.route('/filiais/responsavel/<int:id_responsavel>')
@login_required
def tabela_filiais_por_responsavel(id_responsavel):

    try:   
        # Verifica se o id do responsavel passado como parametro, existe no banco de dados
        responsavel = Responsavel.query.get_or_404(id_responsavel)

        # Paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        
        # Filtra todos as filiais associadas ao responsável e ordena a filial por ordem alfabética
        filiais_responsavel = db.session.query(ResponsavelFilial)\
            .filter_by(id_responsavel=responsavel.id_responsavel)\
            .order_by(ResponsavelFilial.filial.asc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return render_template('/tabelas/associacoes/tabela_filiais_por_responsavel.html', filiais_responsavel=filiais_responsavel)

    except:
        # Exibe um erro específico no flash com detalhes
        flash("Ocorreu um erro ao carregar as filiais por responsavel. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))