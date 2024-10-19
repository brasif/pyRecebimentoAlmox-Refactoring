from flask import render_template, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import Registro, Responsavel, NotaFiscal
from RECEBIMENTO.utils import todos_registros_filtro
from sqlalchemy import desc
from . import tabela_bp


@tabela_bp.route('/registros')
@login_required
def tabela_todos_registros():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Obtém os filtros do formulário
    chave_acesso = request.args.get('chave_acesso')
    nota_fiscal = request.args.get('nota_fiscal')
    filial = request.args.get('filial')
    centro = request.args.get('centro')
    status = request.args.get('status')
    prioridade = request.args.get('prioridade')
    responsavel = request.args.get('responsavel')

    # Consulta para trazer todos os registros
    registros_query = db.session.query(Registro)\
        .join(NotaFiscal)\
        .order_by(desc(Registro.id_registro))

    # Aplica filtros
    registros_query = todos_registros_filtro(
        NotaFiscal,
        Registro,
        Responsavel,
        registros_query,
        chave_acesso,
        nota_fiscal,
        filial,
        centro,
        status,
        prioridade,
        responsavel
    )

    # Pagina os resultados
    registros = registros_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tabelas/tabela_todos_registros.html', registros=registros)
