from flask import render_template, redirect, url_for, flash
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import MudarStatusForm
from RECEBIMENTO.models import NotaFiscal, Registro
from RECEBIMENTO.utils.status_registro import REGISTRO_STATUS_CHOICES
from flask_login import login_required, current_user
from . import mudar_status_bp


# Rota para criar novo registro em Mudar_Status
@mudar_status_bp.route('/<int:id_nota_fiscal>', methods=['GET', 'POST'])
@login_required
def registro_mudar_status(id_nota_fiscal):
    nota_fiscal = NotaFiscal.query.get_or_404(id_nota_fiscal)
    form = MudarStatusForm(obj=nota_fiscal)
    
    try:
        if not REGISTRO_STATUS_CHOICES:
            flash("Nenhum status encontrado. Por favor, abra um chamado para a T.I. para que o problema possa ser solucionado.", "danger")
            form.status.choices = []
        else:
            form.status.choices = [("", "Selecione um status")] + [(status[0], status[1]) for status in REGISTRO_STATUS_CHOICES]


    except SQLAlchemyError as e:
        flash(f"Erro ao acessar o banco de dados ao carregar as empresas: {str(e)}", "danger")
        form.status.choices = []

    except Exception as e:
        flash(f"Erro inesperado ao carregar as opções: {str(e)}", "danger")
        form.status.choices = []


    if form.validate_on_submit():
        try:
            # Cria registro com novo status para a nota fiscal
            recebimento = Registro.criar_registro(form, id_nota_fiscal, current_user.id_responsavel, form.status.data)
            db.session.add(recebimento)
            db.session.commit()

            flash('Registro atualizado com sucesso!', 'success')
            return redirect(url_for('tabela.tabela_registros'))

        except ValueError as ve:
            db.session.rollback()
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f"Erro inesperado: {str(e)}", "danger")

    return render_template('/mudar_status/registro_mudar_status.html', form=form, nota_fiscal=nota_fiscal)
