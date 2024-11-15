from flask import render_template, flash, request, current_app
from flask_login import login_required
from RECEBIMENTO.models.tb_auditoria_models import Auditoria
from RECEBIMENTO.models import Responsavel
from RECEBIMENTO.utils import auditoria_filtro
from . import tabela_bp


@tabela_bp.route('/auditoria')
@login_required
def tabela_auditoria():

    try:
        current_app.logger.info("Acessando a rota '/auditoria' - tabela_bp.")
        
        # Dicionários para renomeação
        acoes = {
            "INSERT": "Criação",
            "UPDATE": "Edição",
            "DELETE": "Exclusão",
        }

        tabelas = {
            "tb_responsavel": "Responsável",
            "tb_responsavel_filial": "Responsável x filial",
            "tb_nota_fiscal": "Nota fiscal",
        }

        # Paginação com valores padrão
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        if page < 1 or per_page <= 0:
            raise ValueError("Os valores de página e itens por página devem ser maiores que zero.")
        
        # Filtros com valores da requisição
        filtros = {
            'acao': request.args.get('acao', None),
            'tabela': request.args.get('tabela', None),
            'coluna_alterada': request.args.get('coluna_alterada', None),
            'responsavel': request.args.get('responsavel', None),
            'data_evento': request.args.get('data_evento', None),
        }

        current_app.logger.info(f"Filtros aplicados: {filtros}")
        
        # Consulta de auditoria com filtros
        query = auditoria_filtro(Auditoria, Responsavel, **filtros)

        # Ordenação por id e paginação
        auditoria = query.order_by(Auditoria.id_auditoria.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        current_app.logger.info("Consulta realizada com sucesso.")
        return render_template('/tabelas/tabela_auditoria.html', acoes=acoes, tabelas=tabelas, auditoria=auditoria)

    except ValueError as ve:
        current_app.logger.warning(f"Erro de validação: {ve}")
        flash(str(ve), "warning")
        return render_template('/tabelas/tabela_auditoria.html', acoes=[], tabelas=[], auditoria=[])

    except Exception as e:
        current_app.logger.exception("Erro ao carregar os registros de auditoria.")
        flash("Ocorreu um erro ao carregar os registros de auditoria. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/tabela_auditoria.html', acoes=[], tabelas=[], auditoria=[])
