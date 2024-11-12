from flask import render_template, abort, request
from RECEBIMENTO import db
from flask_login import login_required, current_user
from RECEBIMENTO.utils import responsaveis_por_filial_filtro
from RECEBIMENTO.models import ResponsavelFilial, Responsavel, Filiais
from . import associacoes_bp


@associacoes_bp.route('/responsaveis/filial/<string:filial>')
@login_required
def tabela_responsaveis_por_filial(filial):
    try:
        filial_enum = Filiais[filial]  # Tenta obter a filial do Enum
    except KeyError:
        abort(404)  # Se não encontrar, retorna erro 404

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Parâmetros de filtro
    nome = request.args.get('nome')
    email = request.args.get('email')
    permissao = request.args.get('permissao')
    status = request.args.get('status')
    
    # Consulta para trazer os responsáveis por filial com filtros opcionais
    query = db.session.query(ResponsavelFilial).join(Responsavel).filter(ResponsavelFilial.filial == filial_enum)
    
    
    # Chama a função de filtro de responsáveis com os parâmetros da requisição
    query = responsaveis_por_filial_filtro(
        Responsavel,
        nome,
        email,
        permissao,
        status
    )

    # Ordenação por nome (A-Z)
    responsaveis = query\
        .order_by(Responsavel.nome_responsavel.asc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("/tabelas/associacoes/tabela_responsaveis_por_filial.html", responsaveis=responsaveis, filial=filial_enum, id_responsavel=current_user.id_responsavel)
