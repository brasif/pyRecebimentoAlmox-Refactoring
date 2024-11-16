from RECEBIMENTO import db
import logging

# Configuração do logger
logging.basicConfig(level=logging.ERROR)


def responsaveis_filtro(model, nome, email, permissao, status):
    
    try:
        query = db.session.query(model)

        if nome:
            query = query.filter(model.nome_responsavel.ilike(f'%{nome}%'))

        if email:
            query = query.filter(model.email.ilike(f'%{email}%'))

        if permissao:
            query = query.filter(model.permissao == (permissao.lower() == 'true'))

        if status:
            query = query.filter(model.status == (status.lower() == 'true'))

        return query

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro na aplicação dos filtros de responsáveis: {e}")
        return db.session.query(model)
