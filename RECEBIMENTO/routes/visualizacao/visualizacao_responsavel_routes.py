from flask import render_template
from flask_login import login_required
from RECEBIMENTO.models import Responsavel
from . import visualizacao_bp


@visualizacao_bp.route('/visualizacao/responsavel/<int:id_responsavel>', methods=['GET'])
@login_required
def visualizar_responsavel(id_responsavel):
    responsavel = Responsavel.query.get_or_404(id_responsavel)
    filiais_associadas = responsavel.responsavel_filial
    return render_template('visualizacao/visualizar_responsavel.html', responsavel=responsavel, filiais=filiais_associadas)
