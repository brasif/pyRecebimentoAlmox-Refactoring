from flask import render_template, request, flash
from flask_login import login_required, current_user
from RECEBIMENTO.models import Responsavel
from RECEBIMENTO.utils import responsaveis_filtro
from . import tabela_bp


@tabela_bp.route('/responsaveis')
@login_required
def tabela_responsaveis():
    
    try:
        # Paginação com valores padrão
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Filtros com valores da requisição
        filtros = {
            'nome': request.args.get('nome', None),
            'email': request.args.get('email', None),
            'permissao': request.args.get('permissao', None),
            'status': request.args.get('status', None)
        }

        # Chama a função de filtro com os parâmetros da requisição
        query = responsaveis_filtro(Responsavel, **filtros)

        # Paginação e ordenação por nome do responsável
        responsaveis = query.order_by(Responsavel.nome_responsavel.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return render_template('/tabelas/tabela_responsaveis.html', responsaveis=responsaveis, id_responsavel_logado=current_user.id_responsavel)

    except:
        flash("Ocorreu um erro ao carregar os responsáveis. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/tabela_responsaveis.html', responsaveis=[])
