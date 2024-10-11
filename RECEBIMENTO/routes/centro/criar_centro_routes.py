from flask import render_template, redirect, url_for, flash
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import CentroForm
from RECEBIMENTO.models import Centro
from flask_login import login_required
from . import centro_bp


# Rota para criar um novo centro
@centro_bp.route('/cadastro', methods=['GET', 'POST'])
@login_required
def criar_centro():
    form = CentroForm()

    if form.validate_on_submit():
        try:
            # Cria uma nova instância de Centro usando o método cadastro_centro
            novo_centro = Centro.criar_centro(form)
            db.session.add(novo_centro)
            db.session.commit()

            flash('Centro criado com sucesso!', 'success')
            return redirect(url_for('menu.menu'))

        except ValueError as ve:
            db.session.rollback()
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f"Erro inesperado: {str(e)}", "danger")

    return render_template('/centro/criar_centro.html', form=form)
