from flask import render_template, redirect, flash, request
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import ResponsavelForm
from RECEBIMENTO.models import Responsavel
from flask_login import login_required
from . import responsavel_bp


# Rota para editar um responsável existente
@responsavel_bp.route('/editar/<int:id_responsavel>', methods=['GET', 'POST'])
@login_required
def editar_responsavel(id_responsavel):
    responsavel = Responsavel.query.get_or_404(id_responsavel)
    form = ResponsavelForm(obj=responsavel)

    
    if form.validate_on_submit():
        try:
            # Atualiza os dados do responsável
            Responsavel.atualizacao_responsavel(responsavel, form)
            db.session.commit()

            flash('Responsável atualizado com sucesso!', 'success')
            return redirect(request.referrer)
        
        except ValueError as ve:
            db.session.rollback()
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f"Erro inesperado: {str(e)}", "danger")

    return render_template('/responsavel/editar_responsavel.html', form=form, responsavel=responsavel)
