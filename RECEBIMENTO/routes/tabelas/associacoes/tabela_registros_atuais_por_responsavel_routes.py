from flask import render_template, redirect, url_for, flash, request, current_app
from RECEBIMENTO import db
from flask_login import login_required
from sqlalchemy import func
from RECEBIMENTO.models import Responsavel, Registro, NotaFiscal
from RECEBIMENTO.utils import registros_atuais_por_responsavel_filtro
from . import associacoes_bp


@associacoes_bp.route('/registros/responsavel/<int:id_responsavel>')
@login_required
def tabela_registros_atuais_por_responsavel(id_responsavel):

    try:
        current_app.logger.info(f"Acessando a rota '/registros/responsavel/{id_responsavel}' - associacoes_bp.")

        # Validação do responsável
        responsavel = Responsavel.query.get_or_404(id_responsavel)
        current_app.logger.info(f"Responsável encontrado: {responsavel.nome_responsavel} (ID: {id_responsavel})")

        # Paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        if page < 1 or per_page <= 0:
            raise ValueError("Os valores de página e itens por página devem ser maiores que zero.")

        # Subconsulta
        subquery = db.session.query(
            Registro.id_nota_fiscal,
            func.max(Registro.data_criacao).label('max_data_criacao')
        ).group_by(Registro.id_nota_fiscal).subquery()

        # Consulta principal
        query_base = db.session.query(Registro).filter_by(id_responsavel=id_responsavel).join(
            subquery,
            (Registro.id_nota_fiscal == subquery.c.id_nota_fiscal) & (Registro.data_criacao == subquery.c.max_data_criacao)
        ).join(NotaFiscal)

        # Filtros
        filtros = {
            'mes': request.args.get('mes'),
            'chave_acesso': request.args.get('chave_acesso'),
            'nota_fiscal': request.args.get('nota_fiscal'),
            'filial': request.args.get('filial'),
            'centro': request.args.get('centro'),
            'prioridade': request.args.get('prioridade'),
            'status': request.args.get('status'),
            'data_recebimento': request.args.get('data_recebimento'),
            'data_guarda': request.args.get('data_guarda')
        }
        current_app.logger.info(f"Filtros aplicados: {filtros}")
        registros_query = registros_atuais_por_responsavel_filtro(NotaFiscal, Registro, query_base, **filtros)

        # Paginação e ordenação
        registros = registros_query.order_by(Registro.id_registro.asc()).paginate(page=page, per_page=per_page, error_out=False)

        current_app.logger.info("Consulta realizada com sucesso.")
        return render_template('/tabelas/associacoes/tabela_registros_atuais_por_responsavel.html', registros=registros, nome_responsavel=responsavel.nome_responsavel, id_responsavel=responsavel.id_responsavel)

    except ValueError as ve:
        current_app.logger.warning(f"Erro de validação: {ve}")
        flash(str(ve), "warning")
        return redirect(url_for('menu.menu'))

    except Exception as e:
        current_app.logger.exception("Erro ao carregar registros atuais por responsável.")
        flash("Ocorreu um erro ao carregar os registros atuais por responsável. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))
