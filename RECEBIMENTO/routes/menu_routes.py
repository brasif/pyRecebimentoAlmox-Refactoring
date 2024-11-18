from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import ChaveAcessoForm
from RECEBIMENTO.models import NotaFiscal
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
                # Verifica se a função retorna um valor falso
                if operacao_recebimento(chave_acesso) == False:
                    current_app.logger.warning(f"Falha no recebimento: chave de acesso {chave_acesso}")
                    return redirect(request.referrer)
                else:
                    current_app.logger.info(f"Recebimento registrado com sucesso: chave de acesso {chave_acesso}")
                    return redirect(url_for("nota_fiscal.criar_nota_fiscal", chave_acesso=chave_acesso))
            
            # Mudar status
            elif acao == "mudar_status":
                if operacao_mudar_status(chave_acesso) == False:
                    current_app.logger.warning(f"Falha ao mudar status: chave de acesso {chave_acesso}")
                    return redirect(request.referrer)
                else:
                    nota_fiscal = NotaFiscal.query.filter_by(chave_acesso=chave_acesso).first_or_404()
                    current_app.logger.info(f"Status da nota fiscal {nota_fiscal.id_nota_fiscal} alterado com sucesso")
                    return redirect(url_for("mudar_status.registro_mudar_status", id_nota_fiscal=nota_fiscal.id_nota_fiscal))
            
            # Estorno
            elif acao == "estorno":
                if operacao_estorno(chave_acesso) == False:
                    current_app.logger.warning(f"Falha no estorno: chave de acesso {chave_acesso}")
                    return redirect(request.referrer)
                else:
                    nota_fiscal = NotaFiscal.query.filter_by(chave_acesso=chave_acesso).first_or_404()
                    current_app.logger.info(f"Estorno da nota fiscal {nota_fiscal.id_nota_fiscal} realizado com sucesso")
                    return redirect(url_for("estorno.registro_estorno", id_nota_fiscal=nota_fiscal.id_nota_fiscal))
        
        except ValueError as ve:
            current_app.logger.error(f"Erro de valor: {str(ve)}")
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            current_app.logger.error(f"Erro ao acessar o banco de dados: {str(e)}")
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            current_app.logger.error(f"Erro inesperado: {str(e)}")
            flash(f"Erro inesperado: {str(e)}", "danger")
    
    return render_template("/index.html", form=form, id_responsavel=current_user.id_responsavel)
