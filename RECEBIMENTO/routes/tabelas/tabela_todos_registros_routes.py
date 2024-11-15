from flask import render_template, request
from flask_login import login_required
from RECEBIMENTO.models import Registro, Responsavel, NotaFiscal
from RECEBIMENTO.utils import todos_registros_filtro
from . import tabela_bp


@tabela_bp.route('/registros')
@login_required
def tabela_todos_registros():
    
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Chama a função de filtro de todos os registros com os parâmetros da requisição
    registros_query = todos_registros_filtro(
        Registro,
        NotaFiscal,
        Responsavel,
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

    return render_template('/tabelas/tabela_todos_registros.html', registros=registros)
