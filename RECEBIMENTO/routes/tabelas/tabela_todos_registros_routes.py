from flask import render_template, flash, request, current_app
from flask_login import login_required
from RECEBIMENTO.models import Registro, Responsavel, NotaFiscal
from RECEBIMENTO.utils import todos_registros_filtro
from . import tabela_bp


@tabela_bp.route('/registros')
@login_required
def tabela_todos_registros():

    try:
        current_app.logger.info("Acessando a rota '/registros' - tabela_bp.")
        
        # Paginação com valores padrão
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        if page < 1 or per_page <= 0:
            raise ValueError("Os valores de página e itens por página devem ser maiores que zero.")
        
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
            'data_guarda': request.args.get('data_guarda', None),
        }

        current_app.logger.info(f"Filtros aplicados: {filtros}")
        
        # Consulta de registros com filtros
        registros_query = todos_registros_filtro(Registro, NotaFiscal, Responsavel, **filtros)

        # Paginação e ordenação por id do registro
        registros = registros_query.order_by(Registro.id_registro.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        current_app.logger.info("Consulta realizada com sucesso.")
        return render_template('/tabelas/tabela_todos_registros.html', registros=registros)

    except ValueError as ve:
        current_app.logger.warning(f"Erro de validação: {ve}")
        flash(str(ve), "warning")
        return render_template('/tabelas/tabela_todos_registros.html', registros=[])

    except Exception as e:
        current_app.logger.exception("Erro ao carregar todos os registros.")
        flash("Ocorreu um erro ao carregar todos os registros. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/tabela_todos_registros.html', registros=[])
