from flask import render_template, request
from RECEBIMENTO import db
from sqlalchemy import func
from flask_login import login_required
from RECEBIMENTO.models import Responsavel, Registro, NotaFiscal
from RECEBIMENTO.utils import registros_atuais_por_responsavel_filtro
from . import associacoes_bp


@associacoes_bp.route('/registros/responsavel/<int:id_responsavel>')
@login_required
def tabela_registros_atuais_por_responsavel(id_responsavel):
    responsavel = Responsavel.query.get_or_404(id_responsavel)

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)


    # Obtém os filtros do formulário
    mes = request.args.get('mes')
    data_recebimento = request.args.get('data_recebimento')
    chave_acesso = request.args.get('chave_acesso')
    nota_fiscal = request.args.get('nota_fiscal')
    filial = request.args.get('filial')
    centro = request.args.get('centro')
    status = request.args.get('status')
    data_guarda = request.args.get('data_guarda')
    prioridade = request.args.get('prioridade')


    # Subconsulta para encontrar o último registro por id_nota_fiscal
    subquery = db.session.query(
        Registro.id_nota_fiscal,
        func.max(Registro.data_criacao).label('max_data_criacao')
    ).group_by(Registro.id_nota_fiscal).subquery()

    # Consulta principal para trazer os registros mais recentes por id_nota_fiscal
    registros_query = db.session.query(Registro)\
        .filter_by(id_responsavel=id_responsavel)\
        .join(subquery, (Registro.id_nota_fiscal == subquery.c.id_nota_fiscal) & (Registro.data_criacao == subquery.c.max_data_criacao))\
        .join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)\
        .order_by(Registro.data_criacao.desc())
    
    
    # Aplica filtros
    registros_query = registros_atuais_por_responsavel_filtro(
        NotaFiscal,
        Registro,
        registros_query,
        mes,
        chave_acesso,
        nota_fiscal,
        filial,
        centro,
        status,
        prioridade,
        data_recebimento,
        data_guarda
    )
    
    # Pagina os resultados
    registros = registros_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tabelas/associacoes/tabela_registros_atuais_por_responsavel.html', registros=registros, nome_responsavel=responsavel.nome_responsavel, id_responsavel=responsavel.id_responsavel)
