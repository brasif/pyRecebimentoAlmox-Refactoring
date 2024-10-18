from flask import render_template, redirect, url_for, flash, request
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import MudarStatusForm
from RECEBIMENTO.models import NotaFiscal, Registro, Responsavel, ResponsavelFilial
from RECEBIMENTO.utils import operacao_mudar_status, REGISTRO_STATUS_CHOICES
from flask_login import login_required
from . import mudar_status_bp


# Rota para criar novo registro em Mudar_Status
@mudar_status_bp.route("/<int:id_nota_fiscal>", methods=["GET", "POST"])
@login_required
def registro_mudar_status(id_nota_fiscal):
    nota_fiscal = NotaFiscal.query.get_or_404(id_nota_fiscal)
    
    # Verifica se a função retorna um valor falso
    if operacao_mudar_status(nota_fiscal.chave_acesso) == False:
        # Redireciona para a ultima página acessada
        return redirect(request.referrer)
    else:
        # A execução continua apenas se não houver redirecionamento na função operacao_mudar_status
        form = MudarStatusForm(obj=nota_fiscal)
        
        ultimo_registro = Registro.query.filter_by(id_nota_fiscal=nota_fiscal.id_nota_fiscal).order_by(Registro.id_registro.desc()).first()
        
        if not ultimo_registro:
            flash("Não foi possível obter o registro da nota fiscal", "danger")
            return redirect(url_for("menu.menu"))
        
        try:
            # Busca os responsáveis vinculados à filial da NF
            responsaveis_vinculados =(Responsavel.query
                .join(ResponsavelFilial)
                .filter(ResponsavelFilial.filial == nota_fiscal.filial, Responsavel.status == True)
                .all()
            )

            if not responsaveis_vinculados:
                flash("Nenhum responsável encontrado nas filiais vinculadas.", "warning")
                form.id_responsavel.choices = []
            else:
                # Preencher choices com os responsáveis vinculados
                form.id_responsavel.choices = [(0, "Selecione um responsável")] + [(resp.id_responsavel, resp.nome_responsavel) for resp in responsaveis_vinculados]
                if request.method == "GET":
                    form.id_responsavel.data = ultimo_registro.id_responsavel

            if not REGISTRO_STATUS_CHOICES:
                flash("Nenhum status encontrado. Por favor, abra um chamado para a T.I. para que o problema possa ser solucionado.", "danger")
                form.status.choices = []
            else:
                # Remove o último status registrado do choices
                status_disponiveis = [status for status in REGISTRO_STATUS_CHOICES if status[0] != ultimo_registro.status_registro]
                form.status.choices = [("", "Selecione um status")] + [(status[0], status[1]) for status in status_disponiveis]
        
        except SQLAlchemyError as e:
            flash(f"Erro ao acessar o banco de dados ao carregar as empresas: {str(e)}", "danger")
            form.id_responsavel.choices = []
            form.status.choices = []

        except Exception as e:
            flash(f"Erro inesperado ao carregar as opções: {str(e)}", "danger")
            form.id_responsavel.choices = []
            form.status.choices = []


        if form.validate_on_submit():
            try:
                # Verifica se o status do forms é o mesmo que o ultimo status registrado
                if form.status.data != ultimo_registro.status_registro:
                    
                    # Cria registro com novo status para a nota fiscal
                    recebimento = Registro.criar_registro(id_nota_fiscal, form.id_responsavel.data, form.status.data)
                    db.session.add(recebimento)
                    db.session.commit()

                    flash("Registro atualizado com sucesso!", "success")
                    return redirect(url_for("menu.menu"))
                else:
                    flash("Insira um status diferente do atual para continuar.", "warning")

            except ValueError as ve:
                db.session.rollback()
                flash(str(ve), "warning")

            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

            except Exception as e:
                db.session.rollback()
                flash(f"Erro inesperado: {str(e)}", "danger")

        return render_template("/mudar_status/registro_mudar_status.html", form=form, nota_fiscal=nota_fiscal, status_atual=ultimo_registro.status_registro)
