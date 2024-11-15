from flask import render_template, abort, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import Filiais, Registro, NotaFiscal, Responsavel
from RECEBIMENTO.utils import todos_registros_por_filial_filtro
from . import associacoes_bp


@associacoes_bp.route('/registros/filial/<string:filial>')
@login_required
def tabela_todos_registros_por_filial(filial):

    # Tenta obter a filial do Enum
    try:
        filial_enum = Filiais[filial]
    except KeyError:
        abort(404) # Se não encontrar, retorna erro 404

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Consulta para trazer todos os registros pela filial do parametro
    query_base = db.session.query(Registro)\
        .join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)\
        .filter(NotaFiscal.filial == filial_enum)

    # Chama a função de filtro de responsáveis por filial com os parâmetros da requisição
    registros_query = todos_registros_por_filial_filtro(
        NotaFiscal,
        Registro,
        Responsavel,
        query_base,
        request.args.get('mes'),
        request.args.get('chave_acesso'),
        request.args.get('nota_fiscal'),
        request.args.get('centro'),
        request.args.get('status'),
        request.args.get('prioridade'),
        request.args.get('responsavel'),
        request.args.get('data_recebimento'),
        request.args.get('data_guarda')
    )

    # Ordenação por id do registro
    registros = registros_query\
        .order_by(Registro.id_registro.asc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tabelas/associacoes/tabela_todos_registros_por_filial.html', registros=registros, filial=filial_enum)
