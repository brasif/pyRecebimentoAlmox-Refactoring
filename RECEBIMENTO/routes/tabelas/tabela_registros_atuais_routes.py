from flask import render_template, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import Registro, NotaFiscal, Responsavel
from RECEBIMENTO.utils import registros_atuais_filtro
from sqlalchemy import func
from . import tabela_bp


@tabela_bp.route('/registros/atuais')
@login_required
def tabela_registros_atuais():
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
    responsavel = request.args.get('responsavel')
    
    
    # Subconsulta para encontrar o último registro por id_nota_fiscal
    subquery = db.session.query(
        Registro.id_nota_fiscal,
        func.max(Registro.data_criacao).label('max_data_criacao')
    ).group_by(Registro.id_nota_fiscal).subquery()

    # Consulta principal para trazer os registros mais recentes por id_nota_fiscal
    registros_query = db.session.query(Registro)\
        .join(subquery, (Registro.id_nota_fiscal == subquery.c.id_nota_fiscal) & (Registro.data_criacao == subquery.c.max_data_criacao))\
        .join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)\
        .order_by(Registro.data_criacao.desc())
        
    # Aplica filtros
    registros_query = registros_atuais_filtro(
        NotaFiscal,
        Registro,
        Responsavel,
        registros_query,
        mes,
        chave_acesso,
        nota_fiscal,
        filial,
        centro,
        status,
        prioridade,
        responsavel,
        data_recebimento,
        data_guarda
    )
    
    # Pagina os resultados
    registros = registros_query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/tabela_registros_atuais.html', registros=registros)
