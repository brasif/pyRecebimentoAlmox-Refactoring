from flask import render_template, redirect, url_for, abort, flash, request, current_app
from RECEBIMENTO import db
from sqlalchemy import func
from flask_login import login_required, current_user
from RECEBIMENTO.models import Responsavel, Filiais, Registro, NotaFiscal
from RECEBIMENTO.utils import registros_atuais_por_responsavel_e_filial_filtro
from . import associacoes_bp


@associacoes_bp.route('/registros/responsavel/<int:id_responsavel>/filial/<string:filial>')
@login_required
def tabela_registros_atuais_por_responsavel_e_filial(id_responsavel, filial):

    try:
        current_app.logger.info(f"Acessando a rota '/registros/responsavel/{id_responsavel}/filial/{filial}' - associacoes_bp.")

        # Verifica se o id do responsável passado como parâmetro existe no banco de dados
        responsavel = Responsavel.query.get_or_404(id_responsavel)
        current_app.logger.info(f"Responsável encontrado: {responsavel.nome_responsavel}")

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

        # Subconsulta para encontrar o último registro por id_nota_fiscal
        subquery = db.session.query(
            Registro.id_nota_fiscal,
            func.max(Registro.data_criacao).label('max_data_criacao')
        ).group_by(Registro.id_nota_fiscal).subquery()

        # Consulta principal para trazer os registros mais recentes por id_nota_fiscal e filtrar por responsável e filial
        query_base = db.session.query(Registro)\
            .join(subquery, (Registro.id_nota_fiscal == subquery.c.id_nota_fiscal) & (Registro.data_criacao == subquery.c.max_data_criacao))\
            .join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)\
            .filter(Registro.id_responsavel == id_responsavel)\
            .filter(NotaFiscal.filial == filial_enum)

        # Chama a função de filtro de registros por responsável e filial com os parâmetros da requisição
        registros_query = registros_atuais_por_responsavel_e_filial_filtro(
            NotaFiscal,
            Registro,
            query_base,
            request.args.get('mes', None),
            request.args.get('chave_acesso', None),
            request.args.get('nota_fiscal', None),
            request.args.get('centro', None),
            request.args.get('status', None),
            request.args.get('prioridade', None),
            request.args.get('data_recebimento', None),
            request.args.get('data_guarda', None)
        )

        # Ordenação por id do registro
        registros = registros_query\
            .order_by(Registro.id_registro.asc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        current_app.logger.info("Consulta de registros realizada com sucesso.")
        return render_template('/tabelas/associacoes/tabela_registros_atuais_por_responsavel_e_filial.html', registros=registros, nome_responsavel=responsavel.nome_responsavel, id_responsavel=current_user.id_responsavel, filial=filial_enum)

    except ValueError as ve:
        current_app.logger.warning(f"Erro de validação: {ve}")
        flash(str(ve), "warning")
        return redirect(url_for('menu.menu'))

    except Exception as e:
        current_app.logger.exception("Erro ao carregar os registros por responsável e filial.")
        flash("Ocorreu um erro ao carregar os registros. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))
