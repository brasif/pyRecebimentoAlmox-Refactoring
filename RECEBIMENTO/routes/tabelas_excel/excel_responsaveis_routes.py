from flask import current_app, jsonify
from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import Responsavel
from RECEBIMENTO.utils import geracao_excel
from . import tabelas_excel_bp


@tabelas_excel_bp.route('/exportar/responsaveis')
@login_required
def excel_responsaveis():
    
    try:
        current_app.logger.info("Iniciando exportação de responsáveis.")
        
        # Consulta para trazer os responsáveis
        responsaveis = db.session.query(Responsavel).all()

        if not responsaveis:
            current_app.logger.warning("Nenhum responsável encontrado para exportação.")
            return jsonify({'message': 'Nenhum responsável disponível para exportação.'}), 404

        # Criar uma lista de dicionários com os dados para o DataFrame
        data = []
        for responsavel in responsaveis:
            data.append({
                'ID': responsavel.id_responsavel,
                'Nome': responsavel.nome_responsavel or "N/A",
                'E-mail': responsavel.email or "N/A",
                'Permissão': 'Administrador' if responsavel.permissao else 'Usuário',
                'Status': 'Ativo' if responsavel.status else 'Inativo',
                'Data criação': responsavel.data_criacao.strftime('%d/%m/%Y %H:%M') if responsavel.data_criacao else '',
                'Data alteração': responsavel.data_alteracao.strftime('%d/%m/%Y %H:%M') if responsavel.data_alteracao else ''
            })

        current_app.logger.info(f"{len(data)} responsáveis preparados para exportação.")
        return geracao_excel(data, "Responsaveis")
    
    except Exception as e:
        current_app.logger.error(f"Erro ao exportar responsáveis: {e}")
        return jsonify({'message': 'Erro interno ao gerar o arquivo Excel.'}), 500
