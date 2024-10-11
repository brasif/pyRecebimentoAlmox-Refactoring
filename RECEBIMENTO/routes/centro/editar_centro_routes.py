from flask import render_template, redirect, url_for, flash, request
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import CentroForm
from RECEBIMENTO.models import Centro, Filiais
from flask_login import login_required
from . import centro_bp


# Rota para editar um centro existente
@centro_bp.route('/editar/<int:id_centro>', methods=['GET', 'POST'])
@login_required
def editar_centro(id_centro):
    centro = Centro.query.get_or_404(id_centro)
    form = CentroForm(obj=centro)

    try:
        if not Filiais:
            flash("Nenhuma filial encontrada. Por favor, abra um chamado para a T.I. para que o problema possa ser solucionado.", "danger")
            form.filial.choices = []
        else:
            form.filial.choices = [("", "Selecione uma filial")] + [(filial.name, filial.value) for filial in Filiais]
            if request.method == 'GET':
                form.filial.data = centro.filial.name
            
    except SQLAlchemyError as e:
        flash(f"Erro ao acessar o banco de dados ao carregar as empresas: {str(e)}", "danger")
        form.filial.choices = []
        
    except Exception as e:
        flash(f"Erro inesperado ao carregar as opções: {str(e)}", "danger")
        form.filial.choices = []
    
    
    if form.validate_on_submit():
        try:
            # Atualiza os dados do centro
            centro.atualizacao_centro(form)
            db.session.commit()

            flash('Centro atualizado com sucesso!', 'success')
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

    return render_template('/centro/editar_centro.html', form=form, centro=centro)
