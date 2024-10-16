import werkzeug
from flask import render_template, redirect, url_for, flash, request
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.forms import EstornoForm
from RECEBIMENTO.models import NotaFiscal, Registro, Responsavel, ResponsavelFilial
from RECEBIMENTO.utils import operacao_estorno
from flask_login import login_required
from . import estorno_bp


# Rota para criar novo registro com o status "Estorno"
@estorno_bp.route("/<int:id_nota_fiscal>", methods=["GET", "POST"])
@login_required
def registro_estorno(id_nota_fiscal):
    nota_fiscal = NotaFiscal.query.get_or_404(id_nota_fiscal)

    # Valida a chave de acesso para a operação de mudança de status
    validacao = operacao_estorno(nota_fiscal.chave_acesso)
    
    # Verifica se a função retorna um redirecionamento
    if isinstance(validacao, werkzeug.wrappers.Response):
        return validacao
    else:
        # A execução continua apenas se não houver redirecionamento na função operacao_estorno
        form = EstornoForm(obj=nota_fiscal)
        
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
        
        except SQLAlchemyError as e:
            flash(f"Erro ao acessar o banco de dados ao carregar as empresas: {str(e)}", "danger")
            form.id_responsavel.choices = []

        except Exception as e:
            flash(f"Erro inesperado ao carregar as opções: {str(e)}", "danger")
            form.id_responsavel.choices = []


        if form.validate_on_submit():
            try:
                # Verifica se o ultimo status registrado é igual a "Estornado"
                if "Estornado" != ultimo_registro.status_registro:
                    # Cria registro com novo status "Estornado" para a nota fiscal
                    recebimento = Registro.criar_registro(id_nota_fiscal, form.id_responsavel.data, "Estornado")
                    db.session.add(recebimento)
                    db.session.commit()

                    flash("Registro estornado com sucesso!", "success")
                    return redirect(request.referrer)
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

        return render_template("/estorno/registro_estorno.html", form=form, nota_fiscal=nota_fiscal, status_atual=ultimo_registro.status_registro)
