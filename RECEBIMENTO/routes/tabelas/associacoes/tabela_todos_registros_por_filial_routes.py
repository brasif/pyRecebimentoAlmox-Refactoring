from flask import render_template, redirect, url_for, abort, request, flash
from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import Filiais, Registro, NotaFiscal, Responsavel
from RECEBIMENTO.utils import todos_registros_por_filial_filtro
from . import associacoes_bp


@associacoes_bp.route('/registros/filial/<string:filial>')
@login_required
def tabela_todos_registros_por_filial(filial):

    try:
        # Tenta obter a filial do Enum
        try:
            filial_enum = Filiais[filial]
        except KeyError:
            abort(404)  # Se não encontrar, retorna erro 404

        # Paginação com valores padrão
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Filtros com valores da requisição
        filtros = {
            'mes': request.args.get('mes', None),
            'chave_acesso': request.args.get('chave_acesso', None),
            'nota_fiscal': request.args.get('nota_fiscal', None),
            'centro': request.args.get('centro', None),
            'status': request.args.get('status', None),
            'prioridade': request.args.get('prioridade', None),
            'responsavel': request.args.get('responsavel', None),
            'data_recebimento': request.args.get('data_recebimento', None),
            'data_guarda': request.args.get('data_guarda', None)
        }

        # Consulta base para os registros filtrados pela filial
        query_base = db.session.query(Registro)\
            .join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)\
            .filter(NotaFiscal.filial == filial_enum)

        # Chama a função de filtro com os parâmetros da requisição
        registros_query = todos_registros_por_filial_filtro(
            NotaFiscal,
            Registro,
            Responsavel,
            query_base,
            **filtros
        )

        # Ordenação por id do registro
        registros = registros_query\
            .order_by(Registro.id_registro.asc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return render_template('/tabelas/associacoes/tabela_todos_registros_por_filial.html', registros=registros, filial=filial_enum)

    except:
        flash("Ocorreu um erro ao carregar os registros por filial. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))
