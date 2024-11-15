from flask import render_template, request, flash
from flask_login import login_required
from RECEBIMENTO.models import NotaFiscal
from RECEBIMENTO.utils import notas_fiscais_filtro
from . import tabela_bp


@tabela_bp.route('/notas_fiscais')
@login_required
def tabela_notas_fiscais():

    try:
        # Paginação com valores padrão
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Chama a função de filtro de notas fiscais com os parâmetros da requisição
        filtros = {
            'chave_acesso': request.args.get('chave_acesso', None),
            'nota_fiscal': request.args.get('nota_fiscal', None),
            'cnpj': request.args.get('cnpj', None),
            'filial': request.args.get('filial', None),
            'centro': request.args.get('centro', None),
            'prioridade': request.args.get('prioridade', None)
        }

        # Chama a função de filtro com os parâmetros da requisição
        query = notas_fiscais_filtro(NotaFiscal, **filtros)

        # Ordenação por id da nota fiscal
        notas_fiscais = query\
            .order_by(NotaFiscal.id_nota_fiscal.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return render_template('/tabelas/tabela_notas_fiscais.html', notas_fiscais=notas_fiscais)

    except:
        flash("Ocorreu um erro ao carregar as notas fiscais. Tente novamente mais tarde.", "danger")
        return render_template('/tabelas/tabela_notas_fiscais.html', notas_fiscais=[])
