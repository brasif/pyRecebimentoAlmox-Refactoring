from flask import render_template, redirect, url_for, flash, request, current_app
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import NotaFiscalForm
from RECEBIMENTO.models import NotaFiscal, Filiais, ResponsavelFilial, CENTROS_POR_FILIAL
from flask_login import login_required, current_user
from . import nota_fiscal_bp


# Rota para editar nota fiscal
@nota_fiscal_bp.route('/editar/<int:id_nota_fiscal>', methods=['GET', 'POST'])
@login_required
def editar_nota_fiscal(id_nota_fiscal):
    
    nota_fiscal = NotaFiscal.query.get_or_404(id_nota_fiscal)
    form = NotaFiscalForm(obj=nota_fiscal)
    
    try:
        # Busca as filiais associadas ao responsável logado
        current_app.logger.info(f"Buscando filiais vinculadas ao responsável ID {current_user.id_responsavel}")
        filiais_vinculadas = db.session.query(ResponsavelFilial).filter_by(id_responsavel=current_user.id_responsavel).all()

        if not filiais_vinculadas:
            flash("Nenhuma filial vinculada ao responsável.", "warning")
            form.filial.choices = []
            current_app.logger.warning(f"Nenhuma filial encontrada para o responsável ID {current_user.id_responsavel}")
        else:
            form.filial.choices = [("", "Selecione uma filial")] + [(filial.filial.name, filial.filial.value) for filial in filiais_vinculadas]
            current_app.logger.info(f"Filiais vinculadas carregadas com sucesso para o responsável ID {current_user.id_responsavel}")

            # Se for uma requisição 'GET' e a filial já vinculada for associada ao responsável logado
            if request.method == 'GET' and any(filial.filial == nota_fiscal.filial for filial in filiais_vinculadas):
                form.filial.data = nota_fiscal.filial.name

        centros = [centro for centros in CENTROS_POR_FILIAL.values() for centro in centros]
        if request.method == 'GET' and any(filial.filial == nota_fiscal.filial for filial in filiais_vinculadas):
            centros = CENTROS_POR_FILIAL.get(Filiais[nota_fiscal.filial.name], [])
            form.nome_centro.choices = [("", "Selecione um centro")] + [(centro, centro) for centro in centros]
            form.nome_centro.data = nota_fiscal.nome_centro
        
        if not centros:
            form.centro.choices = [("", "Selecione um centro")]
        else:
            form.nome_centro.choices = [("", "Selecione um centro")] + [(centro, centro) for centro in centros]

    except SQLAlchemyError as e:
        current_app.logger.error(f"Erro ao acessar o banco de dados: {str(e)}")
        flash(f"Erro ao acessar o banco de dados ao carregar as empresas: {str(e)}", "danger")
        form.nome_centro.choices = []
        form.filial.choices = []
        
    except Exception as e:
        current_app.logger.error(f"Erro inesperado ao carregar as opções: {str(e)}")
        flash(f"Erro inesperado ao carregar as opções: {str(e)}", "danger")
        form.nome_centro.choices = []
        form.filial.choices = []
    
    
    if form.validate_on_submit():
        try:
            # Atualiza os dados da nota fiscal
            current_app.logger.info(f"Iniciando atualização da nota fiscal ID {id_nota_fiscal}")
            nota_fiscal = NotaFiscal.atualizacao_nota_fiscal(nota_fiscal, form)
            db.session.commit()
            current_app.logger.info(f"Nota fiscal ID {id_nota_fiscal} atualizada com sucesso")

            flash('Nota fiscal atualizada com sucesso!', 'success')
            return redirect(url_for("menu.menu"))

        except ValueError as ve:
            db.session.rollback()
            current_app.logger.warning(f"Erro de validação ao atualizar a nota fiscal ID {id_nota_fiscal}: {str(ve)}")
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao acessar o banco de dados ao atualizar a nota fiscal ID {id_nota_fiscal}: {str(e)}")
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro inesperado ao atualizar a nota fiscal ID {id_nota_fiscal}: {str(e)}")
            flash(f"Erro inesperado: {str(e)}", "danger")

    return render_template('/nota_fiscal_e_recebimento/editar_nota_fiscal.html', form=form, nota_fiscal=nota_fiscal)
