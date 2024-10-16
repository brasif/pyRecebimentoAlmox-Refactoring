from flask import send_file
import io
import pandas as pd


def geracao_excel(data, nome_arquivo):
    # Criar um DataFrame usando pandas
    df = pd.DataFrame(data)

    # Criar um objeto de buffer de memória para o arquivo Excel
    output = io.BytesIO()
    
    # Escrever o DataFrame no buffer como um arquivo Excel
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=nome_arquivo)
    
    # Configurar o ponteiro do buffer para o início do arquivo
    output.seek(0)

    # Enviar o arquivo para o usuário
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=f'{nome_arquivo}.xlsx')