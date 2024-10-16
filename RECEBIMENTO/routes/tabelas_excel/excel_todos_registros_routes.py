from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import Registro
from RECEBIMENTO.utils import geracao_excel
from . import tabelas_excel_bp


@tabelas_excel_bp.route('/exportar/registros')
@login_required
def excel_registros_todos():
    # Consulta para trazer os registros
    registros = db.session.query(Registro).all()

    # Criar uma lista de dicionários com os dados para o DataFrame
    data = [{
        'ID': registro.id_registro,
        'Mês': str.title(registro.mes),
        'Data recebimento': registro.data_recebimento.strftime('%d/%m/%Y %H:%M') if registro.data_recebimento else '',
        'Chave de acesso': registro.nota_fiscal.chave_acesso,
        'Nota Fiscal': registro.nota_fiscal.numero_nf,
        'Filial': registro.nota_fiscal.filial.value,
        'Centro': registro.nota_fiscal.nome_centro,
        'Status': registro.status_registro,
        'Data guarda': registro.data_guarda.strftime('%d/%m/%Y %H:%M') if registro.data_guarda else '',
        'Prioridade': 'Sim' if registro.nota_fiscal.prioridade else 'Não',
        'Resp. Atualização': registro.responsavel.nome_responsavel,
        'Data criação': registro.data_criacao.strftime('%d/%m/%Y %H:%M') if registro.data_criacao else ''
    } for registro in registros]

    return geracao_excel(data, "Registros")
