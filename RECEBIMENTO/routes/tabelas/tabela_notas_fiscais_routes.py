from flask import render_template, request
from flask_login import login_required
from RECEBIMENTO.models import NotaFiscal
from RECEBIMENTO.utils import notas_fiscais_filtro
from sqlalchemy import desc
from . import tabela_bp


@tabela_bp.route('/notas_fiscais')
@login_required
def tabela_notas_fiscais():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Chama a função de filtro de notas fiscais com os parâmetros da requisição
    query = notas_fiscais_filtro(
        NotaFiscal,
        request.args.get('chave_acesso', None),
        request.args.get('nota_fiscal', None),
        request.args.get('cnpj', None),
        request.args.get('filial', None),
        request.args.get('centro', None),
        request.args.get('prioridade', None)
    )

    # Ordenação por data de alteração e depois por filial
    notas_fiscais = query\
        .order_by(desc(NotaFiscal.data_alteracao), NotaFiscal.filial.asc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('/tabelas/tabela_notas_fiscais.html', notas_fiscais=notas_fiscais)