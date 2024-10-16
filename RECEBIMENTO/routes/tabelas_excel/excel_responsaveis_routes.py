from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import Responsavel
from RECEBIMENTO.utils import geracao_excel
from . import tabelas_excel_bp


@tabelas_excel_bp.route('/exportar/responsaveis')
@login_required
def excel_responsaveis():
    # Consulta para trazer os responsáveis
    responsaveis = db.session.query(Responsavel).all()

    # Criar uma lista de dicionários com os dados para o DataFrame
    data = [{
        'ID': responsavel.id_responsavel,
        'Nome': responsavel.nome_responsavel,
        'E-mail': responsavel.email,
        'Permissão': 'Administrador' if responsavel.permissao else 'Usuário',
        'Status': 'Ativo' if responsavel.status else 'Inativo',
        'Data criação': responsavel.data_criacao.strftime('%d/%m/%Y %H:%M') if responsavel.data_criacao else '',
        'Data alteração': responsavel.data_alteracao.strftime('%d/%m/%Y %H:%M') if responsavel.data_alteracao else ''
    } for responsavel in responsaveis]

    return geracao_excel(data, "Responsaveis")
