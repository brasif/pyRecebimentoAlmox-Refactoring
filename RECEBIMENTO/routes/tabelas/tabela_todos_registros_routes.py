from flask import render_template, request, flash
from flask_login import login_required
from RECEBIMENTO.models import Registro, Responsavel, NotaFiscal
from RECEBIMENTO.utils import todos_registros_filtro
from . import tabela_bp


@tabela_bp.route('/registros')
@login_required
def tabela_todos_registros():

    try:
        # Paginação com valores padrão
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Filtros com valores da requisição
        filtros = {
            'mes': request.args.get('mes', None),
            'chave_acesso': request.args.get('chave_acesso', None),
            'nota_fiscal': request.args.get('nota_fiscal', None),
            'filial': request.args.get('filial', None),
            'centro': request.args.get('centro', None),
            'status': request.args.get('status', None),
            'prioridade': request.args.get('prioridade', None),
            'responsavel': request.args.get('responsavel', None),
            'data_recebimento': request.args.get('data_recebimento', None),
            'data_guarda': request.args.get('data_guarda', None)
        }

        # Chama a função de filtro com os parâmetros da requisição
        registros_query = todos_registros_filtro(Registro, NotaFiscal, Responsavel, **filtros)

        # Paginação e ordenação por id do registro
        registros = registros_query.order_by(Registro.id_registro.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return render_template('/tabelas/tabela_todos_registros.html', registros=registros)

    except:
        flash("Ocorreu um erro ao carregar todos os registros. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/tabela_todos_registros.html', registros=[])
