from RECEBIMENTO import db
from flask_login import login_required
from RECEBIMENTO.models import Responsavel
import io
import pandas as pd
from flask import send_file
from RECEBIMENTO.models import NotaFiscal
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
        'Centro': nota_fiscal.nome_centro
    } for nota_fiscal in notas_fiscais]

    # Criar um DataFrame usando pandas
    df = pd.DataFrame(data)

    # Criar um objeto de buffer de memória para o arquivo Excel
    output = io.BytesIO()
    
    # Escrever o DataFrame no buffer como um arquivo Excel
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Notas Fiscais')
    
    # Configurar o ponteiro do buffer para o início do arquivo
    output.seek(0)

    # Enviar o arquivo para o usuário
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name='notas_fiscais.xlsx')
