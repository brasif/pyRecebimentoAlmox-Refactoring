from flask import render_template, redirect, flash, request, current_app
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import ResponsavelFilialForm
from RECEBIMENTO.models import ResponsavelFilial, Responsavel, Filiais
from flask_login import login_required
from . import responsavel_filial_bp


# Rota para editar uma relação responsavel_filial existente
@responsavel_filial_bp.route('/editar/<int:id_responsavel_filial>', methods=['GET', 'POST'])
@login_required
def editar_responsavel_filial(id_responsavel_filial):
    
    current_app.logger.info(f"Acessando a rota '/editar/{id_responsavel_filial}' - responsavel_filial_bp.")
    responsavel_filial = ResponsavelFilial.query.get_or_404(id_responsavel_filial)
    form = ResponsavelFilialForm(obj=responsavel_filial)
    
    try:
        responsaveis = Responsavel.query.filter_by(status=True).all()
        if not responsaveis:
            current_app.logger.warning("Nenhum responsável encontrado para vinculação.")
            flash("Nenhum responsável encontrado. Por favor, cadastre um responsável antes de registrar uma relação 'responsável x filial'.", "warning")
            form.id_responsavel.choices = []
        else:
            form.id_responsavel.choices = [(0, "Selecione um responsável")] + [(responsavel.id_responsavel, responsavel.nome_responsavel) for responsavel in responsaveis]
        
        if not Filiais:
            current_app.logger.error("Nenhuma filial encontrada.")
            flash("Nenhuma filial encontrada. Por favor, abra um chamado para a T.I. para que o problema possa ser solucionado.", "danger")
            form.filial.choices = []
        else:
            form.filial.choices = [("", "Selecione uma filial")] + [(filial.name, filial.value) for filial in Filiais]
            if request.method == 'GET':
                form.filial.data = responsavel_filial.filial.name
                current_app.logger.info("Carregando os dados da filial para edição.")
        
    except SQLAlchemyError as e:
        current_app.logger.error(f"Erro ao acessar o banco de dados: {str(e)}")
        flash(f"Erro ao acessar o banco de dados ao carregar as empresas: {str(e)}", "danger")
        form.id_responsavel.choices = []
        form.filial.choices = []
        
    except Exception as e:
        current_app.logger.error(f"Erro inesperado ao carregar as opções: {str(e)}")
        flash(f"Erro inesperado ao carregar as opções: {str(e)}", "danger")
        form.id_responsavel.choices = []
        form.filial.choices = []
    
    
    if form.validate_on_submit():
        try:
            current_app.logger.info("Atualizando os dados do vínculo.")
            ResponsavelFilial.atualizacao_responsavel_filial(responsavel_filial, form)
            db.session.commit()
            current_app.logger.info("Vínculo atualizado com sucesso.")
            flash('Vínculo entre colaborador e filial atualizado com sucesso!', 'success')
            return redirect(request.referrer)

        except ValueError as ve:
            db.session.rollback()
            current_app.logger.warning(f"Erro de validação: {str(ve)}")
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao acessar o banco de dados: {str(e)}")
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro inesperado: {str(e)}")
            flash(f"Erro inesperado: {str(e)}", "danger")

    current_app.logger.info("Renderizando o template de edição.")
    return render_template('/responsavel_filial/editar_responsavel_filial.html', form=form, responsavel_filial=responsavel_filial)
