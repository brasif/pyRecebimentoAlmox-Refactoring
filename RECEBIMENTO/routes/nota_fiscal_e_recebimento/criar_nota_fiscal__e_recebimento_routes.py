from flask import render_template, redirect, url_for, flash
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import NotaFiscalRecebimentoForm
from RECEBIMENTO.models import NotaFiscal, ResponsavelFilial, Responsavel, Registro, CENTROS_POR_FILIAL
from RECEBIMENTO.utils import definicao_status_recebimento
from flask_login import login_required, current_user
from . import nota_fiscal_bp


@nota_fiscal_bp.route('/recebimento/cadastro', methods=['GET', 'POST'])
@login_required
def criar_nota_fiscal():
    form = NotaFiscalRecebimentoForm()
    
    try:
        # Busca as filiais associadas ao responsável logado
        filiais_vinculadas = db.session.query(ResponsavelFilial).filter_by(id_responsavel=current_user.id_responsavel).all()

        if not filiais_vinculadas:
            flash("Nenhuma filial vinculada ao responsável.", "warning")
            form.filial.choices = []
        else:
            form.filial.choices = [("", "Selecione uma filial")] + [(filial.filial.name, filial.filial.value) for filial in filiais_vinculadas]

            # Lista de filiais vinculadas (extraindo o valor de 'filial' do enum)
            filiais = [filial.filial for filial in filiais_vinculadas]

            # Busca os responsáveis associados às mesmas filiais vinculadas ao responsável logado
            responsaveis_vinculados = db.session.query(Responsavel).join(ResponsavelFilial).filter(ResponsavelFilial.filial.in_(filiais)).all()

            if not responsaveis_vinculados:
                flash("Nenhum responsável encontrado nas filiais vinculadas.", "warning")
                form.id_responsavel.choices = []
            else:
                # Preencher choices com os responsáveis vinculados
                form.id_responsavel.choices = [(0, "Selecione um responsável")] + [(resp.id_responsavel, resp.nome_responsavel) for resp in responsaveis_vinculados]

        # Busca os centros
        centros = [centro for centros in CENTROS_POR_FILIAL.values() for centro in centros]
        if not centros:
            form.nome_centro.choices = [("", "Selecione um centro")]
        else:
            form.nome_centro.choices = [("", "Selecione um centro")] + [(centro, centro) for centro in centros]

    except SQLAlchemyError as e:
        flash(f"Erro ao acessar o banco de dados ao carregar as empresas: {str(e)}", "danger")
        form.nome_centro.choices = []
        form.id_responsavel.choices = []
        form.filial.choices = []
        
    except Exception as e:
        flash(f"Erro inesperado ao carregar as opções: {str(e)}", "danger")
        form.nome_centro.choices = []
        form.id_responsavel.choices = []
        form.filial.choices = []
    

    if form.validate_on_submit():
        try:
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
        
    return render_template('/nota_fiscal_e_recebimento/criar_nota_fiscal_e_recebimento.html', form=form)
