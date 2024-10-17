from flask import render_template, abort
from flask_login import login_required
from RECEBIMENTO.models import Filiais, CENTROS_POR_FILIAL
from . import gerenciamento_filial_bp


# Rota para menu do gerenciamento de filial
@gerenciamento_filial_bp.route("/<string:filial>", methods=["GET", "POST"])
@login_required
def menu_filial(filial):
    try:
        filial_enum = Filiais[filial]  # Tenta obter a filial do Enum
    except KeyError:
        abort(404)  # Se não encontrar, retorna erro 404

    # Busca os centros associados à filial no dicionário
    centros = CENTROS_POR_FILIAL.get(filial_enum, [])

    return render_template("/gerenciamento_filial/menu_filial.html", filial=filial_enum, centros=centros)
