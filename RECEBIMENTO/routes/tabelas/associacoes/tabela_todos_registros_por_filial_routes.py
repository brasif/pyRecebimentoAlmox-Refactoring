from flask import render_template, abort, request
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import Filiais, Registro, NotaFiscal, Responsavel
from RECEBIMENTO.utils import todos_registros_por_filial_filtro
from . import associacoes_bp


@associacoes_bp.route('/registros/filial/<string:filial>')
@login_required
def tabela_todos_registros_por_filial(filial):
    try:
        filial_enum = Filiais[filial]  # Tenta obter a filial do Enum
    except KeyError:
        abort(404)  # Se não encontrar, retorna erro 404

    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Obtém os filtros do formulário
    mes = request.args.get('mes')
    chave_acesso = request.args.get('chave_acesso')
    nota_fiscal = request.args.get('nota_fiscal')
    centro = request.args.get('centro')
    status = request.args.get('status')
    prioridade = request.args.get('prioridade')
    responsavel = request.args.get('responsavel')
    data_recebimento = request.args.get('data_recebimento')
    data_guarda = request.args.get('data_guarda')


    # Consulta para trazer todos os registros por filial
    registros_query = db.session.query(Registro)\
        .join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)\
        .filter(NotaFiscal.filial == filial_enum)\
        .order_by(Registro.id_registro.desc())


    # Aplica filtros
    registros_query = todos_registros_por_filial_filtro(
        NotaFiscal,
        Registro,
        Responsavel,
        registros_query,
        mes,
        chave_acesso,
        nota_fiscal,
        centro,
        status,
        prioridade,
        responsavel,
        data_recebimento,
        data_guarda
    )

    # Pagina os resultados
    registros = registros_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tabelas/associacoes/tabela_todos_registros_por_filial.html', registros=registros, filial=filial_enum)
