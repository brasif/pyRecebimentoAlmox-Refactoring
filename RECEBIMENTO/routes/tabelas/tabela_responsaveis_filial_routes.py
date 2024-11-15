from flask import render_template, flash, request, current_app
from flask_login import login_required
from RECEBIMENTO.models import ResponsavelFilial, Responsavel
from RECEBIMENTO.utils import responsaveis_filial_filtro
from . import tabela_bp


@tabela_bp.route('/responsaveis_filial')
@login_required
def tabela_responsaveis_filial():

    try:
        current_app.logger.info("Acessando a rota '/responsaveis_filial'.")

        # Paginação com valores padrão e validação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        if page < 1 or per_page < 1:
            raise ValueError("Os valores de página e itens por página devem ser maiores que zero.")

        # Filtros com valores da requisição
        filtros = {
            'filial': request.args.get('filial', None),
            'nome': request.args.get('nome', None),
            'email': request.args.get('email', None),
            'permissao': request.args.get('permissao', None),
            'status': request.args.get('status', None)
        }

        current_app.logger.info(f"Filtros aplicados: {filtros}")

        # Chama a função de filtro com os parâmetros da requisição
        query = responsaveis_filial_filtro(ResponsavelFilial, Responsavel, **filtros)

        # Paginação e ordenação por filial e nome do responsável
        responsaveis_filial = query.order_by(
            ResponsavelFilial.filial.asc(),
            Responsavel.nome_responsavel.asc()
        ).paginate(page=page, per_page=per_page, error_out=False)

        current_app.logger.info("Consulta realizada com sucesso.")
        return render_template('/tabelas/tabela_responsaveis_filial.html', responsaveis_filial=responsaveis_filial)

    except ValueError as e:
        current_app.logger.error(f"Erro de validação: {str(e)}")
        flash(str(e), "danger")
        return render_template('/tabelas/tabela_responsaveis_filial.html', responsaveis_filial=[])
    
    except Exception as e:
        current_app.logger.exception("Erro ao carregar os responsáveis por filial.")
        flash("Ocorreu um erro ao carregar os responsáveis por filial. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/tabela_responsaveis_filial.html', responsaveis_filial=[])
