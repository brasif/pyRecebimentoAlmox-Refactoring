from flask import render_template, redirect, flash, request, current_app
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import ResponsavelFilialForm
from RECEBIMENTO.models import ResponsavelFilial, Responsavel, Filiais
from flask_login import login_required
from . import responsavel_filial_bp


# Rota para criar um novo registro de responsável por filial
@responsavel_filial_bp.route('/cadastro', methods=['GET', 'POST'])
@login_required
def criar_responsavel_filial():
    
    current_app.logger.info("Acessando a rota '/cadastro' - responsavel_filial_bp.")
    form = ResponsavelFilialForm()
    
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
            current_app.logger.info("Carregando as opções de filial para o formulário.")
        
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
            current_app.logger.info("Criando um novo vínculo.")
            novo_responsavel_filial = ResponsavelFilial.criar_responsavel_filial(form)
            db.session.add(novo_responsavel_filial)
            db.session.commit()
            current_app.logger.info("Vínculo criado com sucesso.")
            flash('Vínculo entre colaborador e filial criado com sucesso!', 'success')
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

    current_app.logger.info("Renderizando o template de criação.")
    return render_template('/responsavel_filial/criar_responsavel_filial.html', form=form)
