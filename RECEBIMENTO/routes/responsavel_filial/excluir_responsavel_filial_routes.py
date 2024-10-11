from flask import redirect, url_for, flash
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.models import ResponsavelFilial
from flask_login import login_required
from . import responsavel_filial_bp


# Rota para excluir um registro de responsável por filial
@responsavel_filial_bp.route('/excluir/<int:id_responsavel_filial>', methods=['POST'])
@login_required
def excluir_responsavel_filial(id_responsavel_filial):
    
    responsavel_filial = ResponsavelFilial.query.get_or_404(id_responsavel_filial)
    
    try:
        db.session.delete(responsavel_filial)
        db.session.commit()
        flash("Vinculo responável por filial excluído com sucesso", "success")
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
    
    
    return redirect(url_for('tabela.tabela_responsaveis_filial'))
