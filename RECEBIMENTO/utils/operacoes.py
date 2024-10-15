from flask import flash, redirect, url_for
from RECEBIMENTO.models import NotaFiscal, Registro
from sqlalchemy.exc import SQLAlchemyError


# ========== Chave de acesso ==========

# Validação da chave de acesso
def validacao_chave_acesso(chave_acesso):
    try:
        # Retorna se a chave de acesso tiver 44 caracteres e for um número inteiro
        return len(chave_acesso) == 44 and chave_acesso.isdigit()
    except Exception as e:
        # Caso haja erro
        raise ValueError(f"Erro na validação da chave de acesso: {str(e)}")

# Obter número da NF a partir da chave de acesso
def obter_numero_nf(chave_acesso):
    try:
        # Valida a chave de acesso
        if validacao_chave_acesso(chave_acesso):
            # Retorna o número da NF
            return chave_acesso[27:34]
        else:
            flash("ERRO: Não foi possível obter o número da NF, chave de acesso inválida!", "danger")
            return redirect(url_for("menu.menu"))
    except Exception as e:
        # Caso haja erro
        raise ValueError(f"Erro na extração do número da NF a partir da chave de acesso: {str(e)}")


# ========== OPERAÇÕES ==========

# HANDLER RECEBIMENTO
def operacao_recebimento(chave_acesso):
    try:
        if validacao_chave_acesso(chave_acesso):
            # Busca a nota fiscal no banco de dados
            nota_fiscal = NotaFiscal.query.filter_by(chave_acesso=chave_acesso).first()
            
            # Verifica se a chave de acesso já existe no banco de dados
            if nota_fiscal:
                
                # Busca o último registro na tabela de registro referente ao ID da NF
                registro = Registro.query.filter_by(id_nota_fiscal=nota_fiscal.id_nota_fiscal).order_by(Registro.id_registro.desc()).first()
                
                # Verifica se existe registro no banco de dados
                if registro:
                    # Verifica se o último status registrado da nota é igual a "Estornado"
                    if registro.status_registro == "Estornado":
                        return redirect(url_for("nota_fiscal.criar_nota_fiscal", chave_acesso=chave_acesso))
                    else:
                        flash("A chave de acesso já foi registrada anteriormente.", "warning")
                        return redirect(url_for("menu.menu"))
                else:
                    flash(f"ERRO: Abra um chamado para a T.I., não foi possível encontrar um registro referente à nota fiscal. ID NF: {nota_fiscal.id_nota_fiscal}", "danger")
                    return redirect(url_for("menu.menu"))
            else:
                return redirect(url_for("nota_fiscal.criar_nota_fiscal", chave_acesso=chave_acesso))
        else:
            flash("Por favor, insira uma chave de acesso válida para continuar.", "warning")
            return redirect(url_for("menu.menu"))
    
    except ValueError as ve:
        flash(str(ve), "warning")
        return redirect(url_for("menu.menu"))

    except SQLAlchemyError as e:
        flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")
        return redirect(url_for("menu.menu"))

    except Exception as e:
        flash(f"Erro inesperado: {str(e)}", "danger")
        return redirect(url_for("menu.menu"))


# HANDLER MUDAR STATUS
def operacao_mudar_status(chave_acesso):
    try:
        if validacao_chave_acesso(chave_acesso):
            # Busca a nota fiscal no banco de dados
            nota_fiscal = NotaFiscal.query.filter_by(chave_acesso=chave_acesso).first()
            
            # Verifica se a chave de acesso já existe no banco de dados
            if nota_fiscal:
                
                # Busca o último registro na tabela de registro referente ao ID da NF
                registro = Registro.query.filter_by(id_nota_fiscal=nota_fiscal.id_nota_fiscal).order_by(Registro.id_registro.desc()).first()
                
                # Verifica se existe registro no banco de dados
                if registro:
                    # Verifica se o último status registrado da nota é igual a "Estornado"
                    if registro.status_registro == "Estornado":
                        flash("A NF foi estornada. Por favor, registre o Recebimento novamente para continuar.", "warning")
                        return redirect(url_for("menu.menu"))
                    else:
                        return redirect(url_for("nota_fiscal.criar_nota_fiscal", chave_acesso=chave_acesso))
                else:
                    flash(f"ERRO: Abra um chamado para a T.I., não foi possível encontrar um registro referente à nota fiscal. ID NF: {nota_fiscal.id_nota_fiscal}", "danger")
                    return redirect(url_for("menu.menu"))
            else:
                flash("A chave de acesso não foi cadastrada anteriormente. Por favor, registre o recebimento.", "warning")
                return redirect(url_for("menu.menu"))
        else:
            flash("Por favor, insira uma chave de acesso válida para continuar.", "warning")
            return redirect(url_for("menu.menu"))
    
    except ValueError as ve:
        flash(str(ve), "warning")
        return redirect(url_for("menu.menu"))

    except SQLAlchemyError as e:
        flash(f"Erro ao acessar o banco de dados: {str(e)}", "danger")
        return redirect(url_for("menu.menu"))

    except Exception as e:
        flash(f"Erro inesperado: {str(e)}", "danger")
        return redirect(url_for("menu.menu"))
