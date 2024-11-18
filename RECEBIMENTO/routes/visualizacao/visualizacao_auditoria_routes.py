from flask import render_template, redirect, flash, request, current_app
from flask_login import login_required
from RECEBIMENTO.models.tb_auditoria_models import Auditoria
from . import visualizacao_bp


@visualizacao_bp.route('/visualizacao/auditoria/<int:id_auditoria>', methods=['GET'])
@login_required
def visualizar_auditoria(id_auditoria):

    current_app.logger.info("Acessando página de visualização de auditoria")

    auditoria = Auditoria.query.get_or_404(id_auditoria)
    current_app.logger.info(f"Informações da auditoria obtida: {auditoria.id_auditoria}")

    try:
        acoes = {
            "INSERT": "Criação",
            "UPDATE": "Edição",
            "DELETE": "Exclusão"
        }

        tabelas = {
            "tb_responsavel": "Responsável",
            "tb_responsavel_filial": "Responsável x filial",
            "tb_nota_fiscal": "Nota fiscal"
        }

        return render_template('visualizacao/visualizar_auditoria.html', auditoria=auditoria, acoes=acoes, tabelas=tabelas)

    except Exception as e:
        current_app.logger.critical(f"Erro inesperado ao acessar a página de visualização da auditoria {id_auditoria}: {str(e)}")
        flash(f"Erro inesperado: {str(e)}", "danger")
        return redirect(request.referrer)
