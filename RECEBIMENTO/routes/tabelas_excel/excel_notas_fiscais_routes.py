from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import NotaFiscal
from RECEBIMENTO.utils import geracao_excel
from . import tabelas_excel_bp


@tabelas_excel_bp.route('/exportar/notas_fiscais')
@login_required
def excel_notas_fiscais():
    # Consulta para trazer as notas fiscais
    notas_fiscais = db.session.query(NotaFiscal).all()

    # Criar uma lista de dicionários com os dados para o DataFrame
    data = [{
        'ID': nota_fiscal.id_nota_fiscal,
        'Chave de acesso': nota_fiscal.chave_acesso,
        'Nota Fiscal': nota_fiscal.numero_nf,
        'Volumes': nota_fiscal.volumes,
        'Código CTE': nota_fiscal.codigo_cte,
        'CNPJ': nota_fiscal.cnpj,
        'Filial': nota_fiscal.filial.value,
        'Centro': nota_fiscal.nome_centro,
        'Data criação': nota_fiscal.data_cricao.strftime('%d/%m/%Y %H:%M') if nota_fiscal.data_cricao else '',
        'Data alteração': nota_fiscal.data_alteracao.strftime('%d/%m/%Y %H:%M') if nota_fiscal.data_alteracao else ''
    } for nota_fiscal in notas_fiscais]

    return geracao_excel(data, "Notas_Fiscais")
