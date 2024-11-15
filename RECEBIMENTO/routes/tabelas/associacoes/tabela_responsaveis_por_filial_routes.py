from flask import render_template, redirect, url_for, flash, abort, request, current_app
from flask_login import login_required, current_user
from RECEBIMENTO import db
from RECEBIMENTO.models import ResponsavelFilial, Responsavel, Filiais
from RECEBIMENTO.utils import responsaveis_por_filial_filtro
from . import associacoes_bp


@associacoes_bp.route('/responsaveis/filial/<string:filial>')
@login_required
def tabela_responsaveis_por_filial(filial):

    try:
        current_app.logger.info(f"Acessando a rota '/responsaveis/filial/{filial}' - associacoes_bp.")

        # Validação da filial
        try:
            filial_enum = Filiais[filial]
            current_app.logger.info(f"Filial válida: {filial_enum.name}")
        except KeyError:
            current_app.logger.warning(f"Filial inválida: {filial}")
            abort(404)

        # Paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        
        if page < 1 or per_page <= 0:
            raise ValueError("Os valores de página e itens por página devem ser maiores que zero.")

        # Filtros
        filtros = {
            'nome': request.args.get('nome'),
            'email': request.args.get('email'),
            'permissao': request.args.get('permissao'),
            'status': request.args.get('status')
        }
        current_app.logger.info(f"Filtros aplicados: {filtros}")

        # Consulta base
        query_base = db.session.query(ResponsavelFilial).join(Responsavel).filter(ResponsavelFilial.filial == filial_enum)
        responsaveis_query = responsaveis_por_filial_filtro(Responsavel, query_base, **filtros)

        # Paginação e ordenação
        responsaveis = responsaveis_query.order_by(Responsavel.nome_responsavel.asc()).paginate(page=page, per_page=per_page, error_out=False)

        current_app.logger.info("Consulta realizada com sucesso.")
        return render_template('/tabelas/associacoes/tabela_responsaveis_por_filial.html', responsaveis=responsaveis, filial=filial_enum, id_responsavel=current_user.id_responsavel)

    except ValueError as ve:
        current_app.logger.warning(f"Erro de validação: {ve}")
        flash(str(ve), "warning")
        return redirect(url_for('menu.menu'))

    except Exception as e:
        current_app.logger.exception("Erro ao carregar responsáveis por filial.")
        flash("Ocorreu um erro ao carregar os responsáveis por filial. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))
