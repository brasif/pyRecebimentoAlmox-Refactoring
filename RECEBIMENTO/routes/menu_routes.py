from flask import Blueprint, render_template, flash, request
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import ChaveAcessoForm
from RECEBIMENTO.utils import operacao_recebimento, operacao_mudar_status
from flask_login import login_required, current_user


menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/", methods=["GET", "POST"])
@login_required
def menu():
    form = ChaveAcessoForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Obtem qual operação foi selecionada pelo usuário
            acao = request.form.get("acao")
            
            # Verifica se a operação escolhida
            if acao == "registrar":
                # Recebimento
                return operacao_recebimento(form.chave_acesso.data)
            
            elif acao == "mudar_status":
                # Mudar status
                return operacao_mudar_status(form.chave_acesso.data)
            
            elif acao == "estorno":
                # Estorno (None por enquanto)
                return None
        
        except ValueError as ve:
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            flash(f"Erro inesperado: {str(e)}", "danger")
    
    return render_template("/index.html", form=form, id_responsavel=current_user.id_responsavel)
