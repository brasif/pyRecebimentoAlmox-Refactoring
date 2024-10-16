import werkzeug
from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import ChaveAcessoForm
from RECEBIMENTO.utils import operacao_recebimento, operacao_mudar_status, operacao_estorno
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
            
            # Obtem chave de acesso inserida pelo usuário
            chave_acesso = form.chave_acesso.data
            
            # Verifica se a operação escolhida
            # Recebimento
            if acao == "registrar":
                # Valida a chave de acesso para a operação de mudança de status
                validacao = operacao_recebimento(chave_acesso)

                # Verifica se a função retorna um redirecionamento
                if isinstance(validacao, werkzeug.wrappers.Response):
                    # Retorna o redirecionamento
                    return validacao
                else:
                    # Opereção recebimento
                    return redirect(url_for("nota_fiscal.criar_nota_fiscal", chave_acesso=chave_acesso))
            
            # Mudar status
            elif acao == "mudar_status":
                # Valida a chave de acesso para a operação de mudança de status
                validacao = operacao_mudar_status(chave_acesso)
                
                # Verifica se a função retorna um redirecionamento
                if isinstance(validacao, werkzeug.wrappers.Response):
                    # Retorna o redirecionamento
                    return validacao
                else:
                    # Opereção 'mudar status'
                    return redirect(url_for("mudar_status.registro_mudar_status", id_nota_fiscal=validacao.id_nota_fiscal))
            
            # Estorno
            elif acao == "estorno":
                # Valida a chave de acesso para a operação de estorno
                validacao = operacao_estorno(chave_acesso)
                
                # Verifica se a função retorna um redirecionamento
                if isinstance(validacao, werkzeug.wrappers.Response):
                    # Retorna o redirecionamento
                    return validacao
                else:
                    # Operação de estorno
                    return redirect(url_for("estorno.registro_estorno", id_nota_fiscal=validacao.id_nota_fiscal))
        
        except ValueError as ve:
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            flash(f"Erro inesperado: {str(e)}", "danger")
    
    return render_template("/index.html", form=form, id_responsavel=current_user.id_responsavel)
