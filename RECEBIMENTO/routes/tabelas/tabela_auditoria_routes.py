from flask import render_template, request, flash
from flask_login import login_required
from RECEBIMENTO.models.tb_auditoria_models import Auditoria
from RECEBIMENTO.models import Responsavel
from RECEBIMENTO.utils import auditoria_filtro
from . import tabela_bp


@tabela_bp.route('/auditoria')
@login_required
def tabela_auditoria():

    try:
        # Dicionários para renomeação das informações
        acoes = {
            "INSERT": "Criação",
            "UPDATE": "Edição",
            "DELETE": "Exclusão"
        }

        tabelas = {
            "tb_responsavel": "Responsável",
            "tb_responsavel_filial": "Responsável x filial",
            "tb_nota_fiscal": "Nota fiscal"
        }

        # Paginação com valores padrão
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Filtros com valores da requisição
        filtros = {
            'acao': request.args.get('acao', None),
            'tabela': request.args.get('tabela', None),
            'coluna_alterada': request.args.get('coluna_alterada', None),
            'responsavel': request.args.get('responsavel', None),
            'data_evento': request.args.get('data_evento', None)
        }

        # Chama a função de filtro com os parâmetros da requisição
        query = auditoria_filtro(Auditoria, Responsavel, **filtros)

        # Ordenação por id da auditoria e paginação
        auditoria = query\
            .order_by(Auditoria.id_auditoria.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return render_template('/tabelas/tabela_auditoria.html', acoes=acoes, tabelas=tabelas, auditoria=auditoria)

    except:
        flash("Ocorreu um erro ao carregar os registros de auditoria. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/tabela_auditoria.html', acoes=acoes, tabelas=tabelas, auditoria=[])
