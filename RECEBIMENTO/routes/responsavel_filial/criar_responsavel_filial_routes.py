from flask import render_template, redirect, url_for, flash
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
    form = ResponsavelFilialForm()
    
    try:
        responsaveis = Responsavel.query.filter_by(status=True).all()
        if not responsaveis:
            flash("Nenhum responsavel encontrado. Por favor, cadastre um responsavel antes de registrar uma relação 'responsavel x filial'.", "warning")
            form.id_responsavel.choices = []
        else:
            form.id_responsavel.choices = [(0, "Selecione um responsável")] + [(responsavel.id_responsavel, responsavel.nome_responsavel) for responsavel in responsaveis]
        
        if not Filiais:
            flash("Nenhuma filial encontrada. Por favor, abra um chamado para a T.I. para que o problema possa ser solucionado.", "danger")
            form.filial.choices = []
        else:
            form.filial.choices = [("", "Selecione uma filial")] + [(filial.name, filial.value) for filial in Filiais]
        
    except SQLAlchemyError as e:
        flash(f"Erro ao acessar o banco de dados ao carregar as empresas: {str(e)}", "danger")
        form.id_responsavel.choices = []
        form.filial.choices = []
        
    except Exception as e:
        flash(f"Erro inesperado ao carregar as opções: {str(e)}", "danger")
        form.id_responsavel.choices = []
        form.filial.choices = []
    
    
    if form.validate_on_submit():
        try:
            # Cria uma nova instância de Centro usando o método criar_responsavel_filial
            novo_responsavel_filial = ResponsavelFilial.criar_responsavel_filial(form)
            db.session.add(novo_responsavel_filial)
            db.session.commit()

            flash('Vinculo entre colaborador e filial criado com sucesso!', 'success')
            return redirect(url_for('tabela.tabela_responsaveis_filial'))

        except ValueError as ve:
            db.session.rollback()
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f"Erro inesperado: {str(e)}", "danger")

    return render_template('/responsavel_filial/criar_responsavel_filial.html', form=form)
