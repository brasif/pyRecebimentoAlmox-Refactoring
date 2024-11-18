from flask import render_template, redirect, url_for, flash, request, session, current_app
from RECEBIMENTO import login_manager, db
from RECEBIMENTO.models import Responsavel
from flask_login import login_required, logout_user, login_user
from RECEBIMENTO.utils import autenticacao_URL, autenticacao_token
from . import autenticacao_bp
from app_config import Config
import requests


@autenticacao_bp.route("/login", methods=["GET", "POST"])
def login():
    # Log de acesso à página de login
    current_app.logger.info("Acessando página de login")
    return render_template("/autenticacao/autenticacao_login.html", auth_url=autenticacao_URL())


# Rota para receber o token de acesso após a autenticação
@autenticacao_bp.route("/getAToken")
def get_token():
    code = request.args.get("code")
    if not code:
        current_app.logger.warning("Nenhum código de autorização encontrado")
        return "No authorization code found", 400

    # Adquire o token de acesso usando o código de autorização
    result = autenticacao_token(code)

    if "access_token" in result:
        # Obtém as informações do usuário do token
        user_info = result.get("id_token_claims")
        user_email = user_info.get("preferred_username")  # Email do usuário
        user_name = user_info.get("name")  # Nome do usuário
        access_token = result.get("access_token")

        # Define a URL do grupo de e-mail no Microsoft Graph
        group_url = f"https://graph.microsoft.com/v1.0/groups/{Config.GROUP_ID}/members?$select=mail"

        # Cabeçalhos da requisição
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Faz a requisição para obter a lista de membros do grupo
        response = requests.get(group_url, headers=headers)

        # Verifica o sucesso da requisição
        if response.status_code == 200:
            members = response.json().get("value", [])
            # Verifica se o e-mail do usuário está na lista de membros
            if any(member.get("mail") == user_email for member in members):
                # O usuário faz parte do grupo; continue com o login

                # Verifica se o usuário já existe no banco de dados
                user = Responsavel.query.filter_by(email=user_email).first()
                
                if not user:
                    user = Responsavel(
                        nome_responsavel=user_name,
                        email=user_email,
                        id_azure_ad=user_info.get("oid"),
                        permissao=True,
                        status=True
                    )
                    db.session.add(user)
                    db.session.commit()  # Salva o novo usuário no banco
                    current_app.logger.info(f"Novo usuário cadastrado: {user_email}")

                # Faz login do usuário
                login_user(user)
                session['_user_permissao'] = user.permissao
                current_app.logger.info(f"Usuário {user_email} logado com sucesso")
                return redirect(url_for("menu.menu"))
            else:
                # O usuário não faz parte do grupo
                flash(f"Você não tem permissão para acessar a aplicação!", "warning")
                current_app.logger.warning(f"Usuário {user_email} não tem permissão para acessar o sistema")
                return redirect(url_for("autenticacao.login"))
        else:
            # Erro ao acessar a API do Microsoft Graph
            current_app.logger.error(f"Falha ao recuperar membros do grupo: {response.status_code} - {response.text}")
            return f"Failed to retrieve group members: {response.status_code} - {response.text}", 500
    else:
        error = result.get("error")
        error_description = result.get("error_description")
        current_app.logger.error(f"Falha no login: {error} - {error_description}")
        return f"Login failed: {error} - {error_description}", 401


# Logout
@autenticacao_bp.route("/logout")
@login_required
def logout():
    current_app.logger.info("Usuário deslogado com sucesso")
    logout_user()
    session.clear()
    return redirect(url_for("autenticacao.login"))


# Usuário não autenticado
@login_manager.unauthorized_handler
def unauthorized():
    flash("Você precisa estar autenticado para acessar essa página.", "danger")
    return redirect(url_for("autenticacao.login"))
