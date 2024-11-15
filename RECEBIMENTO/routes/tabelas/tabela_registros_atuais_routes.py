from flask import render_template, flash, request, current_app
from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import Registro, NotaFiscal, Responsavel
from RECEBIMENTO.utils import registros_atuais_filtro
from sqlalchemy import func
from . import tabela_bp


@tabela_bp.route('/registros/atuais')
@login_required
def tabela_registros_atuais():

    try:
        current_app.logger.info("Acessando a rota '/registros/atuais'.")

        # Paginação com valores padrão e validação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        if page < 1 or per_page < 1:
            raise ValueError("Os valores de página e itens por página devem ser maiores que zero.")

        # Subconsulta para encontrar o último registro por id_nota_fiscal
        subquery = db.session.query(
            Registro.id_nota_fiscal,
            func.max(Registro.data_criacao).label('max_data_criacao')
        ).group_by(Registro.id_nota_fiscal).subquery()

        # Consulta principal para trazer os registros mais recentes por id_nota_fiscal
        query_base = db.session.query(Registro).join(
            subquery,
            (Registro.id_nota_fiscal == subquery.c.id_nota_fiscal) &
            (Registro.data_criacao == subquery.c.max_data_criacao)
        ).join(NotaFiscal, Registro.id_nota_fiscal == NotaFiscal.id_nota_fiscal)

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

        current_app.logger.info(f"Filtros aplicados: {filtros}")

        # Chama a função de filtro com os parâmetros da requisição
        query = registros_atuais_filtro(Registro, NotaFiscal, Responsavel, query_base, **filtros)

        # Ordenação por id do registro
        registros = query.order_by(
            Registro.id_registro.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

        current_app.logger.info("Consulta realizada com sucesso.")
        return render_template('/tabelas/tabela_registros_atuais.html', registros=registros)

    except ValueError as e:
        current_app.logger.warning(f"Erro de validação: {str(e)}")
        flash(str(e), "warning")
        return render_template('/tabelas/tabela_registros_atuais.html', registros=[])
    
    except Exception as e:
        current_app.logger.exception("Erro ao carregar os registros atuais.")
        flash("Ocorreu um erro ao carregar os registros atuais. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/tabela_registros_atuais.html', registros=[])
