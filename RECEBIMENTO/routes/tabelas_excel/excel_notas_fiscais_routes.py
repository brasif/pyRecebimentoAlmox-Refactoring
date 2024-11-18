from flask import current_app, jsonify
from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import NotaFiscal
from RECEBIMENTO.utils import geracao_excel
from . import tabelas_excel_bp


@tabelas_excel_bp.route('/exportar/notas_fiscais')
@login_required
def excel_notas_fiscais():
    
    try:
        current_app.logger.info("Iniciando a exportação de notas fiscais.")
        
        # Consulta para trazer as notas fiscais
        notas_fiscais = db.session.query(NotaFiscal).all()
        
        if not notas_fiscais:
            current_app.logger.warning("Nenhuma nota fiscal encontrada.")
            return jsonify({'message': 'Nenhuma nota fiscal disponível para exportação.'}), 404

        # Criar uma lista de dicionários com os dados para o DataFrame
        data = []
        for nota_fiscal in notas_fiscais:
            if not nota_fiscal.chave_acesso:
                current_app.logger.warning(f"Nota Fiscal ID {nota_fiscal.id_nota_fiscal} sem chave de acesso.")
            data.append({
                'ID': nota_fiscal.id_nota_fiscal,
                'Chave de acesso': nota_fiscal.chave_acesso or "N/A",
                'Nota Fiscal': nota_fiscal.numero_nf,
                'Volumes': nota_fiscal.volumes,
                'Código CTE': nota_fiscal.codigo_cte,
                'CNPJ': nota_fiscal.cnpj,
                'Filial': nota_fiscal.filial.value if nota_fiscal.filial else "N/A",
                'Centro': nota_fiscal.nome_centro or "N/A",
                'Data criação': nota_fiscal.data_criacao.strftime('%d/%m/%Y %H:%M') if nota_fiscal.data_criacao else '',
                'Data alteração': nota_fiscal.data_alteracao.strftime('%d/%m/%Y %H:%M') if nota_fiscal.data_alteracao else ''
            })

        current_app.logger.info(f"{len(data)} notas fiscais preparadas para exportação.")
        return geracao_excel(data, "Notas_Fiscais")
    
    except Exception as e:
        current_app.logger.error(f"Erro ao exportar notas fiscais: {e}")
        return jsonify({'message': 'Erro interno ao gerar o arquivo Excel.'}), 500
