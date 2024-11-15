from flask import render_template, request
from flask_login import login_required
from RECEBIMENTO.models.tb_auditoria_models import Auditoria
from RECEBIMENTO.models import Responsavel
from RECEBIMENTO.utils import auditoria_filtro
from sqlalchemy import desc
from . import tabela_bp


@tabela_bp.route('/auditoria')
@login_required
def tabela_auditoria():

    # Dicionário para renomeação das informações da coluna acao
    acoes = {
        "INSERT": "Criação",
        "UPDATE": "Edição",
        "DELETE": "Exclusão"
    }

    # Dicionário para renomeação das informações da coluna tabela_referenciada
    tabelas = {
        "tb_responsavel": "Responsável",
        "tb_responsavel_filial": "Responsável x filial",
        "tb_nota_fiscal": "Nota fiscal"
    }

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Chama a função de filtro de auditoria com os parâmetros da requisição
    auditoria_query = auditoria_filtro(
        Auditoria,
        Responsavel,
        request.args.get('acao', None),
        request.args.get('tabela', None),
        request.args.get('coluna_alterada', None),
        request.args.get('responsavel', None),
        request.args.get('data_evento', None)
    )

    # Ordenação por id da auditoria
    auditoria = auditoria_query\
        .order_by(Auditoria.id_auditoria.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tabelas/tabela_auditoria.html', acoes=acoes, tabelas=tabelas, auditoria=auditoria)
