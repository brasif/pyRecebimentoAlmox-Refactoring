from flask import flash, redirect, url_for
from RECEBIMENTO.models import NotaFiscal, Registro
from sqlalchemy.exc import SQLAlchemyError


# ========== Validação chave de acesso ==========

# Validação da chave de acesso
def validacao_chave_acesso(chave_acesso):
    try:
        # Retorna se a chave de acesso tiver 44 caracteres e for um número inteiro
        return len(chave_acesso) == 44 and chave_acesso.isdigit()
    except Exception as e:
        # Caso haja erro
        raise ValueError(f"Erro na validação da chave de acesso: {str(e)}")


# ========== OPERAÇÕES ==========

# Validação da chave de acesso para o Recebimento
def validacao_recebimento(chave_acesso):
    try:
        if validacao_chave_acesso(chave_acesso):
            # Busca a nota fiscal no banco de dados
            nota_fiscal = NotaFiscal.query.filter_by(chave_acesso=chave_acesso).first()
            
            # Verifica se a chave de acesso já existe no banco de dados
            if nota_fiscal:
                
                # Busca o último registro na tabela de registro referente ao ID da NF
                registro = Registro.query.filter_by(id_chave_acesso=nota_fiscal.id_chave_acesso).last()
                
                # Verifica se existe registro no banco de dados
                if registro:
                    
                    # Verifica se o último status registrado da nota é igal a "Estornado"
                    if registro.status == "Estornado":
                        return redirect(url_for("nota_fiscal.criar_nota_fiscal"))
                    else:
                        flash("A chave de acesso já foi registrada anteriormente.", "warning")
                        return redirect(url_for("menu.menu"))
                else:
                    flash(f"ERRO: Abra um chamado para a T.I., não foi possível encontrar um registro referente a nota fiscal. ID NF: {nota_fiscal.id_chave_acesso}", "danger")
                    return redirect(url_for("menu.menu"))
            else:
                return redirect(url_for("nota_fiscal.criar_nota_fiscal"))
        else:
            flash("Por favor, insira uma chave de acesso válida para continuar.", "warning")
            return redirect(url_for("menu.menu"))
    
    except ValueError as ve:
            flash(str(ve), "warning")

    except SQLAlchemyError as e:
            flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")

    except Exception as e:
            flash(f"Erro inesperado: {str(e)}", "danger")