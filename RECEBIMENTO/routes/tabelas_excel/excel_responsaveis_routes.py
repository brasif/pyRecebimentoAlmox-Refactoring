from flask import send_file
import io
import pandas as pd
from flask_login import login_required
from RECEBIMENTO import db
from RECEBIMENTO.models import Responsavel
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
        'Status': 'Ativo' if responsavel.status else 'Inativo'
    } for responsavel in responsaveis]

    # Criar um DataFrame usando pandas
    df = pd.DataFrame(data)

    # Criar um objeto de buffer de memória para o arquivo Excel
    output = io.BytesIO()
    
    # Escrever o DataFrame no buffer como um arquivo Excel
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Responsáveis')
    
    # Configurar o ponteiro do buffer para o início do arquivo
    output.seek(0)

    # Enviar o arquivo para o usuário
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name='responsaveis.xlsx')
