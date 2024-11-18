from flask import render_template, current_app
from flask_login import login_required
from RECEBIMENTO.models import Responsavel
from . import visualizacao_bp


@visualizacao_bp.route('/visualizacao/responsavel/<int:id_responsavel>', methods=['GET'])
@login_required
def visualizar_responsavel(id_responsavel):

    current_app.logger.info("Acessando página de visualização do responsável")

    responsavel = Responsavel.query.get_or_404(id_responsavel)
    current_app.logger.info(f"Informações do responsável obtidas: {responsavel.id_responsavel}")

    return render_template('visualizacao/visualizar_responsavel.html', responsavel=responsavel, filiais=responsavel.responsavel_filial)
