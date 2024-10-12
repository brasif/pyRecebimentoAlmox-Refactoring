from flask import render_template, redirect, url_for, flash
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import NotaFiscalForm
from RECEBIMENTO.models import NotaFiscal, Filiais, CENTROS_POR_FILIAL
from flask_login import login_required
from . import nota_fiscal_bp


# Rota para criar nota fiscal e registrar recebimento
@nota_fiscal_bp.route('/cadastro', methods=['GET', 'POST'])
@login_required
def criar_nota_fiscal():
    form = NotaFiscalForm()
    
    try:
        if not Filiais:
            flash("Nenhuma filial encontrada. Por favor, abra um chamado para a T.I. para que o problema possa ser solucionado.", "danger")
            form.filial.choices = []
        else:
            form.filial.choices = [("", "Selecione uma filial")] + [(filial.name, filial.value) for filial in Filiais]

        centros = [centro for centros in CENTROS_POR_FILIAL.values() for centro in centros]
        if not centros:
            form.centro.choices = [("", "Selecione um centro")]
        else:
            form.nome_centro.choices = [("", "Selecione um centro")] + [(centro, centro) for centro in centros]

    except SQLAlchemyError as e:
        flash(f"Erro ao acessar o banco de dados ao carregar as empresas: {str(e)}", "danger")
        form.nome_centro.choices = []
        form.filial.choices = []
        
    except Exception as e:
        flash(f"Erro inesperado ao carregar as opções: {str(e)}", "danger")
        form.nome_centro.choices = []
        form.filial.choices = []
    
    
    if form.validate_on_submit():
        try:
            # Cria uma nova instância de NotaFiscal usando o método criar_nota_fiscal
            nova_nota_fiscal = NotaFiscal.criar_nota_fiscal(form)
            db.session.add(nova_nota_fiscal)
            db.session.commit()

            flash('Nota fiscal criada com sucesso!', 'success')
            return redirect(url_for('tabela.tabela_notas_fiscais'))

        except ValueError as ve:
            db.session.rollback()
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f"Erro inesperado: {str(e)}", "danger")

    return render_template('/nota_fiscal/criar_nota_fiscal.html', form=form)
