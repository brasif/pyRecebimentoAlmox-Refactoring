from flask import render_template, redirect, url_for, abort, flash, request, current_app
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import NotaFiscal, Filiais
from RECEBIMENTO.utils import notas_fiscais_por_filial_filtro
from . import associacoes_bp


@associacoes_bp.route('/notas_fiscais/filial/<string:filial>')
@login_required
def tabela_notas_fiscais_por_filial(filial):

    try:
        current_app.logger.info(f"Acessando a rota '/notas_fiscais/filial/{filial}' - associacoes_bp.")

        # Tenta obter a filial do Enum
        try:
            filial_enum = Filiais[filial]
            current_app.logger.info(f"Filial encontrada: {filial_enum}")
        except KeyError:
            current_app.logger.error(f"Filial {filial} não encontrada.")
            abort(404)  # Se não encontrar, retorna erro 404

        # Paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        if page < 1 or per_page <= 0:
            raise ValueError("Os valores de página e itens por página devem ser maiores que zero.")

        # Query para buscar as notas fiscais filtradas pela filial
        notas_fiscais_query = db.session.query(NotaFiscal).filter(NotaFiscal.filial == filial_enum)

        # Aplica filtros adicionais à consulta
        notas_fiscais_query = notas_fiscais_por_filial_filtro(
            notas_fiscais_query,
            request.args.get('mes', None),
            request.args.get('data_emissao', None),
            request.args.get('nota_fiscal', None),
            request.args.get('centro', None),
            request.args.get('status', None),
            request.args.get('responsavel', None)
        )

        # Ordena a consulta
        notas_fiscais = notas_fiscais_query.order_by(NotaFiscal.data_emissao.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        current_app.logger.info("Consulta de notas fiscais por filial realizada com sucesso.")
        return render_template('/tabelas/associacoes/tabela_notas_fiscais_por_filial.html', notas_fiscais=notas_fiscais, filial=filial_enum)

    except ValueError as ve:
        current_app.logger.warning(f"Erro de validação: {ve}")
        flash(str(ve), "warning")
        return redirect(url_for('menu.menu'))

    except Exception as e:
        current_app.logger.exception("Erro ao carregar as notas fiscais por filial.")
        flash("Ocorreu um erro ao carregar as notas fiscais. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))
