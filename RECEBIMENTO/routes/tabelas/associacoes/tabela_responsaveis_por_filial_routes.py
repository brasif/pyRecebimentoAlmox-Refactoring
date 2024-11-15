from flask import render_template, redirect, url_for, abort, request, flash
from RECEBIMENTO import db
from flask_login import login_required, current_user
from RECEBIMENTO.utils import responsaveis_por_filial_filtro
from RECEBIMENTO.models import ResponsavelFilial, Responsavel, Filiais
from . import associacoes_bp


@associacoes_bp.route('/responsaveis/filial/<string:filial>')
@login_required
def tabela_responsaveis_por_filial(filial):

    try:
        # Tenta obter a filial do Enum
        try:
            filial_enum = Filiais[filial]
        except KeyError:
            abort(404)  # Se não encontrar, retorna erro 404

        # Paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        
        # Consulta para trazer os responsáveis por filial
        query_base = db.session.query(ResponsavelFilial)\
            .join(Responsavel)\
            .filter(ResponsavelFilial.filial == filial_enum)
        
        # Chama a função de filtro de responsáveis por filial com os parâmetros da requisição
        responsaveis_query = responsaveis_por_filial_filtro(
            Responsavel,
            query_base,
            request.args.get('nome', None),
            request.args.get('email', None),
            request.args.get('permissao', None),
            request.args.get('status', None)
        )

        # Ordenação por nome (A-Z)
        responsaveis = responsaveis_query\
            .order_by(Responsavel.nome_responsavel.asc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return render_template(
            "/tabelas/associacoes/tabela_responsaveis_por_filial.html",
            responsaveis=responsaveis,
            filial=filial_enum,
            id_responsavel=current_user.id_responsavel
        )

    except:
        flash("Ocorreu um erro ao carregar os responsaveis por filial. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))