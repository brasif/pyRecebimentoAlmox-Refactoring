from flask import render_template
from flask_login import login_required
from RECEBIMENTO.models import NotaFiscal
from . import visualizacao_bp


@visualizacao_bp.route('/visualizacao/nota_fiscal/<int:id_nota_fiscal>', methods=['GET'])
@login_required
def visualizar_nota_fiscal(id_nota_fiscal):
    nota_fiscal = NotaFiscal.query.get_or_404(id_nota_fiscal)
    return render_template('visualizacao/visualizar_nota_fiscal.html', nota_fiscal=nota_fiscal)
