from flask import render_template, abort, current_app
from flask_login import login_required
from RECEBIMENTO.models import Filiais, CENTROS_POR_FILIAL
from . import gerenciamento_filial_bp


@gerenciamento_filial_bp.route("/<string:filial>", methods=["GET", "POST"])
@login_required
def menu_filial(filial):
    
    try:
        filial_enum = Filiais[filial]
        current_app.logger.info(f"Filial '{filial}' encontrada.")
    except KeyError:
        current_app.logger.error(f"Filial '{filial}' não encontrada.")
        abort(404)

    centros = CENTROS_POR_FILIAL.get(filial_enum, [])
    current_app.logger.info(f"Centros para filial '{filial}': {centros}")

    return render_template("/gerenciamento_filial/menu_filial.html", filial=filial_enum, centros=centros)
