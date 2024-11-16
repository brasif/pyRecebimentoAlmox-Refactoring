from flask import render_template, flash, request, current_app
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import ResponsavelFilial, Responsavel
from . import associacoes_bp


@associacoes_bp.route('/filiais/responsavel/<int:id_responsavel>')
@login_required
def tabela_filiais_por_responsavel(id_responsavel):

    try:
        current_app.logger.info(f"Acessando a rota '/filiais/responsavel/{id_responsavel}' - associacoes_bp.")

        # Verifica se o id do responsavel passado como parametro, existe no banco de dados
        responsavel = Responsavel.query.get_or_404(id_responsavel)
        current_app.logger.info(f"Responsável encontrado: {responsavel.nome_responsavel}")

        # Paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        
        if page < 1 or per_page <= 0:
            raise ValueError("Os valores de página e itens por página devem ser maiores que zero.")

        # Filtra todos as filiais associadas ao responsável e ordena a filial por ordem alfabética
        filiais_responsavel = db.session.query(ResponsavelFilial)\
            .filter_by(id_responsavel=responsavel.id_responsavel)\
            .order_by(ResponsavelFilial.filial.asc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        current_app.logger.info("Consulta realizada com sucesso.")
        return render_template('/tabelas/associacoes/tabela_filiais_por_responsavel.html', filiais_responsavel=filiais_responsavel)

    except ValueError as ve:
        current_app.logger.warning(f"Erro de validação: {ve}")
        flash(str(ve), "warning")
        return render_template('/tabelas/associacoes/tabela_filiais_por_responsavel.html', filiais_responsavel=[])

    except Exception as e:
        current_app.logger.exception("Erro ao carregar as filiais por responsavel.")
        flash("Ocorreu um erro ao carregar as filiais por responsavel. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/associacoes/tabela_filiais_por_responsavel.html', filiais_responsavel=[])
