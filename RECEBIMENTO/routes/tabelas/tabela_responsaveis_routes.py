from flask import render_template, request
from flask_login import login_required, current_user
from RECEBIMENTO.models import Responsavel
from RECEBIMENTO.utils import responsaveis_filtro
from . import tabela_bp


@tabela_bp.route('/responsaveis')
@login_required
def tabela_responsaveis():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Chama a função de filtro de responsáveis com os parâmetros da requisição
    query = responsaveis_filtro(
        Responsavel,
        request.args.get('nome', None),
        request.args.get('email', None),
        request.args.get('permissao', None),
        request.args.get('status', None)
    )

    # Ordenação por nome (A-Z)
    responsaveis = query\
        .order_by(Responsavel.nome_responsavel.asc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/tabela_responsaveis.html', responsaveis=responsaveis, id_responsavel_logado=current_user.id_responsavel)
