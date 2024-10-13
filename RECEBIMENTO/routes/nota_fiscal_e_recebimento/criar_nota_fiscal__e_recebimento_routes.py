from flask import render_template, redirect, url_for, flash
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import NotaFiscalRecebimentoForm
from RECEBIMENTO.models import NotaFiscal, Filiais, CENTROS_POR_FILIAL, Registro
from RECEBIMENTO.utils import definicao_status_recebimento
from flask_login import login_required, current_user
from . import nota_fiscal_bp


@nota_fiscal_bp.route('/recebimento/cadastro', methods=['GET', 'POST'])
@login_required
def criar_nota_fiscal():
    form = NotaFiscalRecebimentoForm()
    
    try:
        if not Filiais:
            flash("Nenhuma filial encontrada. Por favor, abra um chamado para a T.I. para que o problema possa ser solucionado.", "danger")
            form.filial.choices = []
        else:
            form.filial.choices = [("", "Selecione uma filial")] + [(filial.name, filial.value) for filial in Filiais]

        centros = [centro for centros in CENTROS_POR_FILIAL.values() for centro in centros]
        if not centros:
            form.nome_centro.choices = [("", "Selecione um centro")]
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
            # Inicia uma nova transação manualmente
            nova_nota_fiscal = NotaFiscal.criar_nota_fiscal(form)
            db.session.add(nova_nota_fiscal)
            db.session.flush()  # Envia as mudanças para o banco para gerar o ID
            
            # Acessa o ID da nova nota fiscal corretamente
            id_nota_fiscal = nova_nota_fiscal.id_nota_fiscal
            
            # Cria uma nova instância de Registro
            status = definicao_status_recebimento(form.recusa.data, form.avaria.data)
            recebimento = Registro.criar_registro(form, id_nota_fiscal, current_user.id_responsavel, status)
            db.session.add(recebimento)

            # Comita as alterações
            db.session.commit()

            flash('Registro criado com sucesso!', 'success')
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
    
    # Se houver erros de validação no formulário
    elif form.errors:
        for campo, erros in form.errors.items():
            for erro in erros:
                flash(f'{campo.upper()} ERRO: {erro}', 'warning')

    return render_template('/nota_fiscal_e_recebimento/criar_nota_fiscal_e_recebimento.html', form=form)
