from flask import render_template, redirect, url_for, abort, request, flash
from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import NotaFiscal, Filiais
from RECEBIMENTO.utils import notas_fiscais_por_filial_filtro
from sqlalchemy import desc
from . import associacoes_bp


@associacoes_bp.route('/notas_fiscais/filial/<string:filial>')
@login_required
def tabela_notas_fiscais_por_filial(filial):

    try:
        # Tenta obter a filial do Enum
        try:
            filial_enum = Filiais[filial]
        except KeyError:
            abort(404)  # Se não encontrar, retorna erro 404

        # Paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int) 
        
        # Consulta para trazer as notas fiscais por filial
        query_base = db.session.query(NotaFiscal)\
            .filter_by(filial=filial_enum)\
            .order_by(desc(NotaFiscal.data_alteracao))
        
        # Chama a função de filtro de notas fiscais por filial com os parâmetros da requisição
        notas_fiscais_query = notas_fiscais_por_filial_filtro(
            NotaFiscal,
            query_base,
            request.args.get('chave_acesso', None),
            request.args.get('nota_fiscal', None),
            request.args.get('cnpj', None),
            request.args.get('centro', None),
            request.args.get('prioridade', None)
        )
        
        # Ordenação por id da nota fiscal
        notas_fiscais = notas_fiscais_query\
            .order_by(NotaFiscal.id_nota_fiscal.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return render_template('/tabelas/associacoes/tabela_notas_fiscais_por_filial.html', notas_fiscais=notas_fiscais, filial=filial_enum)
    
    except:
        flash("Ocorreu um erro ao carregar as notas fiscais por filial. Tente novamente mais tarde.", "danger")
        return redirect(url_for('menu.menu'))
