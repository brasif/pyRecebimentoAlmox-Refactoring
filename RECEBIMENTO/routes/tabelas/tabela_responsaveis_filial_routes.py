from flask import render_template, request
from flask_login import login_required
from RECEBIMENTO.models import ResponsavelFilial, Responsavel
from RECEBIMENTO.utils import responsaveis_filial_filtro
from . import tabela_bp


@tabela_bp.route('/responsaveis_filial')
@login_required
def tabela_responsaveis_filial():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Chama a função de filtro de responsáveis por filial com os parâmetros da requisição
    query = responsaveis_filial_filtro(
        ResponsavelFilial,
        Responsavel,
        request.args.get('filial', None), 
        request.args.get('nome', None), 
        request.args.get('email', None), 
        request.args.get('permissao', None), 
        request.args.get('status', None)
    )

    # Ordenação por nome da filial e do responsável
    responsaveis_filial = query\
        .order_by(ResponsavelFilial.filial.asc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tabelas/tabela_responsaveis_filial.html', responsaveis_filial=responsaveis_filial)
