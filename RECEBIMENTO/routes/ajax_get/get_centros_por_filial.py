from flask import request, jsonify
from flask_login import login_required
from RECEBIMENTO.models import Filiais, CENTROS_POR_FILIAL
from . import ajax_get_bp


@ajax_get_bp.route("/get_centros", methods=["GET"])
@login_required
def get_centros():
    filial = request.args.get('filial')

    if not filial:
        return jsonify({"error": "Nenhuma filial selecionada."}), 400

    try:
        # Acessa o enum pela string da filial
        filial_enum = Filiais[filial]
        centros = CENTROS_POR_FILIAL.get(filial_enum, [])

        # Opções de centro
        centros_options = [{'value': centro, 'label': centro} for centro in centros]

        return jsonify(centros_options)

    except KeyError:
        return jsonify({"error": "Filial não encontrada."}), 404
    
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar centros: {str(e)}"}), 500
