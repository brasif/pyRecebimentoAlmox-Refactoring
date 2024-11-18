from flask import render_template, redirect, url_for, flash, request, current_app
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import NotaFiscalRecebimentoForm
from RECEBIMENTO.models import NotaFiscal, ResponsavelFilial, Responsavel, Registro, CENTROS_POR_FILIAL
from RECEBIMENTO.utils import operacao_recebimento, definicao_status_recebimento, obter_numero_nf
from flask_login import login_required, current_user
from . import nota_fiscal_bp


@nota_fiscal_bp.route('/recebimento/cadastro/<string:chave_acesso>', methods=['GET', 'POST'])
@login_required
def criar_nota_fiscal(chave_acesso):

    if operacao_recebimento(chave_acesso) == False:
        current_app.logger.warning(f"Operação de recebimento inválida para chave {chave_acesso}")
        return redirect(request.referrer)

    form = NotaFiscalRecebimentoForm()

    try:
        filiais_vinculadas = db.session.query(ResponsavelFilial).filter_by(id_responsavel=current_user.id_responsavel).all()

        if not filiais_vinculadas:
            current_app.logger.info(f"Responsável ID {current_user.id_responsavel} não possui filiais vinculadas.")
            flash("Nenhuma filial vinculada ao responsável.", "warning")
            form.filial.choices = []
        else:
            form.filial.choices = [("", "Selecione uma filial")] + [(filial.filial.name, filial.filial.value) for filial in filiais_vinculadas]
            filiais = [filial.filial for filial in filiais_vinculadas]
            responsaveis_vinculados = db.session.query(Responsavel).join(ResponsavelFilial).filter(ResponsavelFilial.filial.in_(filiais)).all()

            if not responsaveis_vinculados:
                current_app.logger.info(f"Nenhum responsável encontrado para filiais vinculadas ao responsável ID {current_user.id_responsavel}.")
                flash("Nenhum responsável encontrado nas filiais vinculadas.", "warning")
                form.id_responsavel.choices = []
            else:
                form.id_responsavel.choices = [(0, "Selecione um responsável")] + [(resp.id_responsavel, resp.nome_responsavel) for resp in responsaveis_vinculados]

        centros = [centro for centros in CENTROS_POR_FILIAL.values() for centro in centros]
        form.nome_centro.choices = [("", "Selecione um centro")] + [(centro, centro) for centro in centros]

    except SQLAlchemyError as e:
        current_app.logger.error(f"Erro no banco de dados ao carregar opções para chave {chave_acesso}: {str(e)}")
        flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")
        form.nome_centro.choices = []
        form.id_responsavel.choices = []
        form.filial.choices = []
    except Exception as e:
        current_app.logger.critical(f"Erro inesperado ao carregar opções para chave {chave_acesso}: {str(e)}")
        flash(f"Erro inesperado: {str(e)}", "danger")
        form.nome_centro.choices = []
        form.id_responsavel.choices = []
        form.filial.choices = []

    if form.validate_on_submit():
        try:
            nova_nota_fiscal = NotaFiscal.criar_nota_fiscal(chave_acesso, form)
            db.session.add(nova_nota_fiscal)
            db.session.flush()
            id_nota_fiscal = nova_nota_fiscal.id_nota_fiscal
            status = definicao_status_recebimento(form.recusa.data, form.avaria.data)
            recebimento = Registro.criar_registro(id_nota_fiscal, current_user.id_responsavel, status)
            db.session.add(recebimento)
            db.session.commit()

            current_app.logger.info(f"Nota fiscal e recebimento criados com sucesso para chave {chave_acesso}. ID: {id_nota_fiscal}")
            flash('Recebimento registrado com sucesso!', 'success')
            return redirect(url_for("menu.menu"))

        except ValueError as ve:
            db.session.rollback()
            current_app.logger.warning(f"Erro de validação ao criar nota fiscal para chave {chave_acesso}: {str(ve)}")
            flash(str(ve), "warning")

        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Erro no banco de dados ao criar nota fiscal para chave {chave_acesso}: {str(e)}")
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

        except Exception as e:
            db.session.rollback()
            current_app.logger.critical(f"Erro inesperado ao criar nota fiscal para chave {chave_acesso}: {str(e)}")
            flash(f"Erro inesperado: {str(e)}", "danger")
    
    return render_template('/nota_fiscal_e_recebimento/criar_nota_fiscal_e_recebimento.html', form=form, chave_acesso=chave_acesso, numero_nf=obter_numero_nf(chave_acesso))
