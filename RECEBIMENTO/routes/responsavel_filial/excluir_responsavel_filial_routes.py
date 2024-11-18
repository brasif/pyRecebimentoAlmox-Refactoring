from flask import redirect, flash, request, current_app
from RECEBIMENTO import db
from sqlalchemy.exc import SQLAlchemyError
from RECEBIMENTO.models import ResponsavelFilial
from flask_login import login_required
from . import responsavel_filial_bp


# Rota para excluir um registro de responsável por filial
@responsavel_filial_bp.route('/excluir/<int:id_responsavel_filial>', methods=['POST'])
@login_required
def excluir_responsavel_filial(id_responsavel_filial):
    
    try:
        current_app.logger.info(f"Acessando a rota '/excluir/{id_responsavel_filial}' - responsavel_filial_bp.")

        responsavel_filial = ResponsavelFilial.query.get_or_404(id_responsavel_filial)
        current_app.logger.info(f"Responsável filial encontrado: {responsavel_filial.id_responsavel_filial}")

        db.session.delete(responsavel_filial)
        db.session.commit()

        current_app.logger.info("Vinculo responável por filial excluído com sucesso")
        flash("Vinculo responável por filial excluído com sucesso", "success")
        return redirect(request.referrer)

    except ValueError as ve:
        db.session.rollback()
        current_app.logger.warning(f"Erro de valor ao excluir responsável por filial: {str(ve)}")
        flash(str(ve), "warning")

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Erro de SQLAlchemy ao excluir responsável por filial: {str(e)}")
        flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro inesperado ao excluir responsável por filial: {str(e)}")
        flash(f"Erro inesperado: {str(e)}", "danger")
    
    current_app.logger.info(f"Redirecionando para {request.referrer} após tentativa de exclusão.")
    return redirect(request.referrer)
