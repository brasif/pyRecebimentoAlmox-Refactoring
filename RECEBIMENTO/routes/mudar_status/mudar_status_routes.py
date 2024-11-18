from flask import render_template, redirect, url_for, flash, request, current_app
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import MudarStatusForm
from RECEBIMENTO.models import NotaFiscal, Registro, Responsavel, ResponsavelFilial
from RECEBIMENTO.utils import operacao_mudar_status, REGISTRO_STATUS_CHOICES
from flask_login import login_required
from . import mudar_status_bp


@mudar_status_bp.route("/<int:id_nota_fiscal>", methods=["GET", "POST"])
@login_required
def registro_mudar_status(id_nota_fiscal):
    
    nota_fiscal = NotaFiscal.query.get_or_404(id_nota_fiscal)
    current_app.logger.info(f"Rota registro_mudar_status acessada para NotaFiscal ID: {id_nota_fiscal}")

    if operacao_mudar_status(nota_fiscal.chave_acesso) == False:
        current_app.logger.warning("Operação mudar_status retornou False.")
        return redirect(request.referrer)

    form = MudarStatusForm(obj=nota_fiscal)
    ultimo_registro = Registro.query.filter_by(id_nota_fiscal=nota_fiscal.id_nota_fiscal).order_by(Registro.id_registro.desc()).first()

    if not ultimo_registro:
        flash("Não foi possível obter o registro da nota fiscal", "danger")
        current_app.logger.error("Falha ao obter último registro da NotaFiscal.")
        return redirect(url_for("menu.menu"))

    try:
        responsaveis_vinculados = (
            Responsavel.query
            .join(ResponsavelFilial)
            .filter(ResponsavelFilial.filial == nota_fiscal.filial, Responsavel.status == True)
            .all()
        )
        if not responsaveis_vinculados:
            flash("Nenhum responsável encontrado nas filiais vinculadas.", "warning")
            form.id_responsavel.choices = []
            current_app.logger.warning("Nenhum responsável vinculado encontrado.")
        else:
            form.id_responsavel.choices = [(0, "Selecione um responsável")] + [
                (resp.id_responsavel, resp.nome_responsavel) for resp in responsaveis_vinculados
            ]
            if request.method == "GET":
                form.id_responsavel.data = ultimo_registro.id_responsavel

        if not REGISTRO_STATUS_CHOICES:
            flash("Nenhum status encontrado. Por favor, abra um chamado para a T.I.", "danger")
            form.status.choices = []
            current_app.logger.error("REGISTRO_STATUS_CHOICES está vazio.")
        else:
            status_disponiveis = [status for status in REGISTRO_STATUS_CHOICES if status[0] != ultimo_registro.status_registro]
            form.status.choices = [("", "Selecione um status")] + [(status[0], status[1]) for status in status_disponiveis]
            current_app.logger.info("Choices de status carregadas com sucesso.")

    except SQLAlchemyError as e:
        flash(f"Erro ao acessar o banco de dados ao carregar as empresas: {str(e)}", "danger")
        current_app.logger.error(f"Erro SQLAlchemy: {str(e)}")
        form.id_responsavel.choices = []
        form.status.choices = []

    except Exception as e:
        flash(f"Erro inesperado ao carregar as opções: {str(e)}", "danger")
        current_app.logger.exception("Erro inesperado ao carregar opções.")
        form.id_responsavel.choices = []
        form.status.choices = []

    if form.validate_on_submit():
        try:
            if form.status.data != ultimo_registro.status_registro:
                recebimento = Registro.criar_registro(id_nota_fiscal, form.id_responsavel.data, form.status.data)
                db.session.add(recebimento)
                db.session.commit()
                flash("Registro atualizado com sucesso!", "success")
                current_app.logger.info("Registro atualizado com sucesso.")
                return redirect(url_for("menu.menu"))
            else:
                flash("Insira um status diferente do atual para continuar.", "warning")
                current_app.logger.warning("Status selecionado é igual ao último registrado.")

        except ValueError as ve:
            db.session.rollback()
            flash(str(ve), "warning")
            current_app.logger.warning(f"Erro de validação: {str(ve)}")

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")
            current_app.logger.error(f"Erro SQLAlchemy: {str(e)}")

        except Exception as e:
            db.session.rollback()
            flash(f"Erro inesperado: {str(e)}", "danger")
            current_app.logger.exception("Erro inesperado ao salvar registro.")

    return render_template("/mudar_status/registro_mudar_status.html", form=form, nota_fiscal=nota_fiscal, status_atual=ultimo_registro.status_registro)
