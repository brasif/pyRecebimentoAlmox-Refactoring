from flask import render_template, request, flash
from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import Registro, NotaFiscal, Responsavel
from RECEBIMENTO.utils import registros_atuais_filtro
from sqlalchemy import func
from . import tabela_bp


@tabela_bp.route('/registros/atuais')
@login_required
def tabela_registros_atuais():

    try:
        # Paginação com valores padrão
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Subconsulta para encontrar o último registro por id_nota_fiscal
        subquery = db.session.query(
            Registro.id_nota_fiscal,
            func.max(Registro.data_criacao).label('max_data_criacao')
        ).group_by(Registro.id_nota_fiscal).subquery()

        # Consulta principal para trazer os registros mais recentes por id_nota_fiscal
        query_base = db.session.query(Registro)\
            .join(subquery, (Registro.id_nota_fiscal == subquery.c.id_nota_fiscal) & (Registro.data_criacao == subquery.c.max_data_criacao))\
            .join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)

        # Chama a função de filtro com os parâmetros da requisição
        registros_query = registros_atuais_filtro(
            NotaFiscal,
            Registro,
            Responsavel,
            query_base,
            request.args.get('mes'),
            request.args.get('chave_acesso'),
            request.args.get('nota_fiscal'),
            request.args.get('filial'),
            request.args.get('centro'),
            request.args.get('status'),
            request.args.get('prioridade'),
            request.args.get('responsavel'),
            request.args.get('data_recebimento'),
            request.args.get('data_guarda')
        )

        # Ordenação por id do registro
        registros = registros_query\
            .order_by(Registro.id_registro.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return render_template('/tabelas/tabela_registros_atuais.html', registros=registros)

    except:
        flash("Ocorreu um erro ao carregar os registros. Tente novamente mais tarde.", "error")
        return render_template('/tabelas/tabela_registros_atuais.html', registros=[])
