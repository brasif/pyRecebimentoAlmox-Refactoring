from flask import current_app, jsonify
from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import Registro
from RECEBIMENTO.utils import geracao_excel
from . import tabelas_excel_bp


@tabelas_excel_bp.route('/exportar/registros')
@login_required
def excel_todos_registros():
    
    try:
        current_app.logger.info("Iniciando exportação de todos os registros.")
        
        # Consulta para trazer os registros
        registros = db.session.query(Registro).all()

        if not registros:
            current_app.logger.warning("Nenhum registro encontrado para exportação.")
            return jsonify({'message': 'Nenhum registro disponível para exportação.'}), 404

        # Criar uma lista de dicionários com os dados para o DataFrame
        data = []
        for registro in registros:
            if not registro.nota_fiscal.chave_acesso:
                current_app.logger.warning(f"Registro ID {registro.id_registro} com nota fiscal sem chave de acesso.")
            data.append({
                'ID': registro.id_registro,
                'Mês': str.title(registro.mes),
                'Data recebimento': registro.data_recebimento.strftime('%d/%m/%Y %H:%M') if registro.data_recebimento else '',
                'Chave de acesso': registro.nota_fiscal.chave_acesso or "N/A",
                'Nota Fiscal': registro.nota_fiscal.numero_nf,
                'Filial': registro.nota_fiscal.filial.value if registro.nota_fiscal.filial else "N/A",
                'Centro': registro.nota_fiscal.nome_centro or "N/A",
                'Status': registro.status_registro,
                'Data guarda': registro.data_guarda.strftime('%d/%m/%Y %H:%M') if registro.data_guarda else '',
                'Prioridade': 'Sim' if registro.nota_fiscal.prioridade else 'Não',
                'Resp. Atualização': registro.responsavel.nome_responsavel or "N/A",
                'Data criação': registro.data_criacao.strftime('%d/%m/%Y %H:%M') if registro.data_criacao else ''
            })

        current_app.logger.info(f"{len(data)} registros preparados para exportação.")
        return geracao_excel(data, "Registros")
    
    except Exception as e:
        current_app.logger.error(f"Erro ao exportar registros: {e}")
        return jsonify({'message': 'Erro interno ao gerar o arquivo Excel.'}), 500
