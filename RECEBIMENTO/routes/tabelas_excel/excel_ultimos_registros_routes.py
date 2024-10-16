from flask_login import login_required
from RECEBIMENTO import db
from sqlalchemy import func
from RECEBIMENTO.models import Registro
from RECEBIMENTO.utils import geracao_excel
from . import tabelas_excel_bp


@tabelas_excel_bp.route('/exportar/registros/atuais')
@login_required
def excel_registros_atuais():
    
    # Subconsulta para encontrar o último registro por id_nota_fiscal
    subquery = db.session.query(
        Registro.id_nota_fiscal,
        func.max(Registro.data_criacao).label('max_data_criacao')
    ).group_by(Registro.id_nota_fiscal).subquery()

    # Consulta principal para trazer os registros mais recentes por id_nota_fiscal
    registros = db.session.query(Registro)\
        .join(subquery, (Registro.id_nota_fiscal == subquery.c.id_nota_fiscal) & 
                         (Registro.data_criacao == subquery.c.max_data_criacao))\
        .order_by(Registro.data_criacao.desc())\
        .all()

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

    return geracao_excel(data, "Registros_atuais")
