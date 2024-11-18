from flask import request, current_app, jsonify
from flask_login import login_required
from RECEBIMENTO.models import Responsavel, ResponsavelFilial
from . import ajax_get_bp


@ajax_get_bp.route("/get_responsaveis", methods=["GET"])
@login_required
def get_responsaveis():
    filial = request.args.get('filial')

    if not filial:
        current_app.logger.warning("Nenhuma filial selecionada na requisição.")
        return jsonify({"error": "Nenhuma filial selecionada."}), 400

    try:
        # Busca os responsáveis associados à filial selecionada
        responsaveis = (Responsavel.query
                        .join(ResponsavelFilial)
                        .filter(ResponsavelFilial.filial == filial, Responsavel.status == True)
                        .all())

        # Cria a lista de opções para o dropdown
        responsaveis_options = [{'value': responsavel.id_responsavel, 'label': responsavel.nome_responsavel} for responsavel in responsaveis]

        if not responsaveis_options:
            current_app.logger.warning(f"Nenhum responsável encontrado para a filial {filial}.")
            return jsonify({"error": "Nenhum responsável encontrado para essa filial."}), 404

        current_app.logger.info(f"Responsáveis recuperados para a filial {filial}: {responsaveis_options}")
        return jsonify(responsaveis_options)

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar responsáveis: {str(e)}")
        return jsonify({"error": f"Erro ao buscar responsáveis: {str(e)}"}), 500
