from flask import request, jsonify
from flask_login import login_required
from RECEBIMENTO.models import Responsavel, ResponsavelFilial
from . import nota_fiscal_bp


@nota_fiscal_bp.route("/get_responsaveis", methods=["GET"])
@login_required
def get_responsaveis():
    filial = request.args.get('filial')

    if not filial:
        return jsonify({"error": "Nenhuma filial selecionada."}), 400

    try:
        # Busca os responsáveis associados à filial selecionada
        responsaveis = (Responsavel.query
                        .join(ResponsavelFilial)
                        .filter(ResponsavelFilial.filial == filial, Responsavel.status == True)  # Ajustado para booleano
                        .all())

        # Cria a lista de opções para o dropdown
        responsaveis_options = [{'value': responsavel.id_responsavel, 'label': responsavel.nome_responsavel} for responsavel in responsaveis]

        if not responsaveis_options:
            return jsonify({"error": "Nenhum responsável encontrado para essa filial."}), 404

        return jsonify(responsaveis_options)

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar responsáveis: {str(e)}"}), 500
