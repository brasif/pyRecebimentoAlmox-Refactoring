from flask import render_template, redirect, url_for, flash, abort, request, current_app
from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import Filiais, Registro, NotaFiscal, Responsavel
from RECEBIMENTO.utils import todos_registros_por_filial_filtro
from . import associacoes_bp


@associacoes_bp.route('/registros/filial/<string:filial>')
@login_required
def tabela_todos_registros_por_filial(filial):

    try:
        current_app.logger.info(f"Acessando a rota '/registros/filial/{filial}' - associacoes_bp.")

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
            'mes': request.args.get('mes'),
            'chave_acesso': request.args.get('chave_acesso'),
            'nota_fiscal': request.args.get('nota_fiscal'),
            'centro': request.args.get('centro'),
            'status': request.args.get('status'),
            'prioridade': request.args.get('prioridade'),
            'responsavel': request.args.get('responsavel'),
            'data_recebimento': request.args.get('data_recebimento'),
            'data_guarda': request.args.get('data_guarda')
        }

        current_app.logger.info(f"Filtros aplicados: {filtros}")

        # Consulta base
        query_base = db.session.query(Registro).join(NotaFiscal).filter(NotaFiscal.filial == filial_enum)
        registros_query = todos_registros_por_filial_filtro(NotaFiscal, Registro, Responsavel, query_base, **filtros)

        # Paginação e ordenação
        registros = registros_query.order_by(Registro.id_registro.desc()).paginate(page=page, per_page=per_page, error_out=False)

        current_app.logger.info("Consulta realizada com sucesso.")
        return render_template('/tabelas/associacoes/tabela_todos_registros_por_filial.html', registros=registros, filial=filial_enum)

    except ValueError as ve:
        current_app.logger.warning(f"Erro de validação: {ve}")
        flash(str(ve), "warning")
        return redirect(url_for('menu.menu'))

    except Exception as e:
        current_app.logger.exception("Erro ao carregar registros por filial.")
        flash("Ocorreu um erro ao carregar os registros por filial. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))
