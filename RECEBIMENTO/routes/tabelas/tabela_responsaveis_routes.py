from flask import render_template, flash, request, current_app
from flask_login import login_required, current_user
from RECEBIMENTO.models import Responsavel
from RECEBIMENTO.utils import responsaveis_filtro
from . import tabela_bp


@tabela_bp.route('/responsaveis')
@login_required
def tabela_responsaveis():

    try:
        current_app.logger.info("Acessando a rota '/responsaveis' - tabela_bp.")
        
        # Paginação com valores padrão
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        if page < 1 or per_page <= 0:
            raise ValueError("Os valores de página e itens por página devem ser maiores que zero.")
        
        # Filtros com valores da requisição
        filtros = {
            'nome': request.args.get('nome', None),
            'email': request.args.get('email', None),
            'permissao': request.args.get('permissao', None),
            'status': request.args.get('status', None),
        }

        current_app.logger.info(f"Filtros aplicados: {filtros}")
        
        # Consulta de responsáveis com filtros
        query = responsaveis_filtro(Responsavel, **filtros)

        # Paginação e ordenação por nome
        responsaveis = query.order_by(Responsavel.nome_responsavel.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        current_app.logger.info("Consulta realizada com sucesso.")
        return render_template('/tabelas/tabela_responsaveis.html', responsaveis=responsaveis, id_responsavel_logado=current_user.id_responsavel)

    except ValueError as ve:
        current_app.logger.warning(f"Erro de validação: {ve}")
        flash(str(ve), "warning")
        return render_template('/tabelas/tabela_responsaveis.html', responsaveis=[], id_responsavel_logado=current_user.id_responsavel)

    except Exception as e:
        current_app.logger.exception("Erro ao carregar os responsáveis.")
        flash("Ocorreu um erro ao carregar os responsáveis. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/tabela_responsaveis.html', responsaveis=[], id_responsavel_logado=current_user.id_responsavel)
