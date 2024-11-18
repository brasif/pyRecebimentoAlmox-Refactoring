from flask import request, current_app, jsonify
from flask_login import login_required
from RECEBIMENTO.models import Filiais, CENTROS_POR_FILIAL
from . import ajax_get_bp


@ajax_get_bp.route("/get_centros", methods=["GET"])
@login_required
def get_centros():
    filial = request.args.get('filial')

    if not filial:
        current_app.logger.warning("Nenhuma filial selecionada na requisição.")
        return jsonify({"error": "Nenhuma filial selecionada."}), 400

    try:
        # Acessa o enum pela string da filial
        filial_enum = Filiais[filial]
        centros = CENTROS_POR_FILIAL.get(filial_enum, [])

        # Opções de centro
        centros_options = [{'value': centro, 'label': centro} for centro in centros]

        current_app.logger.info(f"Centros recuperados para a filial {filial}: {centros_options}")
        return jsonify(centros_options)

    except KeyError:
        current_app.logger.error(f"Filial {filial} não encontrada.")
        return jsonify({"error": "Filial não encontrada."}), 404
    
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar centros: {str(e)}")
        return jsonify({"error": f"Erro ao buscar centros: {str(e)}"}), 500
