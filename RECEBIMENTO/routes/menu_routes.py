from flask import Blueprint, render_template
from RECEBIMENTO.forms import ChaveAcessoForm
from flask_login import login_required, current_user


menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/", methods=["GET", "POST"])
@login_required
def menu():
    form = ChaveAcessoForm()
    return render_template("/index.html", form=form, id_responsavel=current_user.id_responsavel)