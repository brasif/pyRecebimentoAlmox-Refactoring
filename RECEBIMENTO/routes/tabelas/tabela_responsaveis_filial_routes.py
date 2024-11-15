from flask import render_template, request, flash
from flask_login import login_required
from RECEBIMENTO.models import ResponsavelFilial, Responsavel
from RECEBIMENTO.utils import responsaveis_filial_filtro
from . import tabela_bp


@tabela_bp.route('/responsaveis_filial')
@login_required
def tabela_responsaveis_filial():

    try:
        # Paginação com valores padrão
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Filtros com valores da requisição
        filtros = {
            'filial': request.args.get('filial'),
            'nome': request.args.get('nome'),
            'email': request.args.get('email'),
            'permissao': request.args.get('permissao'),
            'status': request.args.get('status')
        }

        # Chama a função de filtro com os parâmetros da requisição
        query = responsaveis_filial_filtro(ResponsavelFilial, Responsavel, **filtros)

        # Paginação e ordenação por filial e nome do responsável
        responsaveis_filial = query.order_by(ResponsavelFilial.filial.asc(), Responsavel.nome_responsavel.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return render_template('/tabelas/tabela_responsaveis_filial.html', responsaveis_filial=responsaveis_filial)

    except:
        flash("Ocorreu um erro ao carregar os responsáveis por filial. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/tabela_responsaveis_filial.html', responsaveis_filial=[])
