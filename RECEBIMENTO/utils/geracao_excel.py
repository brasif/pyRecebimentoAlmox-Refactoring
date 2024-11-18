from flask import send_file, current_app
import io
import pandas as pd


def geracao_excel(data, nome_arquivo):
    try:
        if not data:
            current_app.logger.warning("Tentativa de gerar Excel com dados vazios.")
            return None

        # Criar um DataFrame usando pandas
        df = pd.DataFrame(data)

        # Criar um objeto de buffer de memória para o arquivo Excel
        output = io.BytesIO()
        
        # Escrever o DataFrame no buffer como um arquivo Excel
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=nome_arquivo)
        
        # Configurar o ponteiro do buffer para o início do arquivo
        output.seek(0)

        current_app.logger.info(f"Arquivo Excel '{nome_arquivo}' gerado com sucesso.")
        
        # Enviar o arquivo para o usuário
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'{nome_arquivo}.xlsx'
        )
    except Exception as e:
        current_app.logger.error(f"Erro ao gerar arquivo Excel '{nome_arquivo}': {e}")
        raise
