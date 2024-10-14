from flask import render_template, redirect, url_for, flash, request
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import NotaFiscalRecebimentoForm
from RECEBIMENTO.models import NotaFiscal, Filiais, CENTROS_POR_FILIAL
from flask_login import login_required
from . import nota_fiscal_bp


# Rota para editar nota fiscal
@nota_fiscal_bp.route('/editar/<int:id_nota_fiscal>', methods=['GET', 'POST'])
@login_required
def editar_nota_fiscal(id_nota_fiscal):
    nota_fiscal = NotaFiscal.query.get_or_404(id_nota_fiscal)
    form = NotaFiscalRecebimentoForm(obj=nota_fiscal)
    
    try:
        if not Filiais:
            flash("Nenhuma filial encontrada. Por favor, abra um chamado para a T.I. para que o problema possa ser solucionado.", "danger")
            form.filial.choices = []
        else:
            form.filial.choices = [("", "Selecione uma filial")] + [(filial.name, filial.value) for filial in Filiais]
            if request.method == 'GET':
                form.filial.data = nota_fiscal.filial.name

        centros = [centro for centros in CENTROS_POR_FILIAL.values() for centro in centros]
        if request.method == 'GET':
            centros = CENTROS_POR_FILIAL.get(Filiais[nota_fiscal.filial.name], [])
            form.nome_centro.choices = [("", "Selecione um centro")] + [(centro, centro) for centro in centros]
            form.nome_centro.data = nota_fiscal.nome_centro
        
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
            # Atualiza os dados da nota fiscal
            nota_fiscal = NotaFiscal.atualizacao_nota_fiscal(nota_fiscal, form)
            db.session.commit()

            flash('Nota fiscal atualizada com sucesso!', 'success')
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

    return render_template('/nota_fiscal/editar_nota_fiscal.html', form=form, nota_fiscal=nota_fiscal)
