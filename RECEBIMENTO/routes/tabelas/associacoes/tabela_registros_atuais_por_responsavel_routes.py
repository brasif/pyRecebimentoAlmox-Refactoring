from flask import render_template, redirect, url_for, request, flash
from RECEBIMENTO import db
from sqlalchemy import func
from flask_login import login_required
from RECEBIMENTO.models import Responsavel, Registro, NotaFiscal
from RECEBIMENTO.utils import registros_atuais_por_responsavel_filtro
from . import associacoes_bp


@associacoes_bp.route('/registros/responsavel/<int:id_responsavel>')
@login_required
def tabela_registros_atuais_por_responsavel(id_responsavel):
    
    try:
        # Verifica se o id do responsável passado como parâmetro existe no banco de dados
        responsavel = Responsavel.query.get_or_404(id_responsavel)

        # Paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Subconsulta para encontrar o último registro por id_nota_fiscal
        subquery = db.session.query(
            Registro.id_nota_fiscal,
            func.max(Registro.data_criacao).label('max_data_criacao')
        ).group_by(Registro.id_nota_fiscal).subquery()

        # Consulta principal para trazer os registros mais recentes por id_nota_fiscal
        query_base = db.session.query(Registro)\
            .filter_by(id_responsavel=id_responsavel)\
            .join(subquery, (Registro.id_nota_fiscal == subquery.c.id_nota_fiscal) & (Registro.data_criacao == subquery.c.max_data_criacao))\
            .join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)

        # Chama a função de filtro de registros por responsável com os parâmetros da requisição
        registros_query = registros_atuais_por_responsavel_filtro(
            NotaFiscal,
            Registro,
            query_base,
            request.args.get('mes', None),
            request.args.get('chave_acesso', None),
            request.args.get('nota_fiscal', None),
            request.args.get('filial', None),
            request.args.get('centro', None),
            request.args.get('prioridade', None),
            request.args.get('status', None),
            request.args.get('data_recebimento', None),
            request.args.get('data_guarda', None)
        )

        # Ordenação por id do registro
        registros = registros_query\
            .order_by(Registro.id_registro.asc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return render_template(
            '/tabelas/associacoes/tabela_registros_atuais_por_responsavel.html',
            registros=registros,
            nome_responsavel=responsavel.nome_responsavel,
            id_responsavel=responsavel.id_responsavel
        )
    
    except:
        flash("Ocorreu um erro ao carregar os registros atuais por responsavel. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))
