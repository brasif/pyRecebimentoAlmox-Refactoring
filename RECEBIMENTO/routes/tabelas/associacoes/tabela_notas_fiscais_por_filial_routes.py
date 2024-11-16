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
        current_app.logger.info("Consulta base de notas fiscais criada com sucesso.")

        # Aplica filtros adicionais à consulta
        try:
            notas_fiscais_query = notas_fiscais_por_filial_filtro(
                NotaFiscal,
                notas_fiscais_query,
                request.args.get('chave_acesso', None),
                request.args.get('nota_fiscal', None),
                request.args.get('cnpj', None),
                request.args.get('centro', None),
                request.args.get('prioridade', None)
            )

            current_app.logger.info("Filtros aplicados com sucesso à consulta de notas fiscais.")
        except Exception as filter_error:
            current_app.logger.error(f"Erro ao aplicar filtros: {filter_error}")
            raise

        # Ordena e pagina a consulta
        notas_fiscais = notas_fiscais_query \
            .order_by(NotaFiscal.data_criacao.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)

        current_app.logger.info("Consulta de notas fiscais paginada com sucesso.")
        return render_template('/tabelas/associacoes/tabela_notas_fiscais_por_filial.html', notas_fiscais=notas_fiscais, filial=filial_enum)

    except ValueError as ve:
        current_app.logger.warning(f"Erro de validação: {ve}")
        flash(str(ve), "warning")
        return redirect(url_for('gerenciamento_filial.menu_filial'))

    except Exception as e:
        current_app.logger.exception("Erro ao carregar as notas fiscais por filial.")
        flash("Ocorreu um erro ao carregar as notas fiscais. Tente novamente mais tarde.", "danger")
        return redirect(url_for('gerenciamento_filial.menu_filial'))
