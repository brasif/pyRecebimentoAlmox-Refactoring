from RECEBIMENTO import db
import logging

# Configuração do logger
logging.basicConfig(level=logging.ERROR)


def responsaveis_filial_filtro(model, join_model, filial, nome, email, permissao, status):
    
    try:
        query = db.session.query(model).join(join_model, model.id_responsavel == join_model.id_responsavel)

        if filial:
            query = query.filter(model.filial == filial)

        if nome:
            query = query.filter(join_model.nome_responsavel.ilike(f'%{nome}%'))

        if email:
            query = query.filter(join_model.email.ilike(f'%{email}%'))

        if permissao:
            query = query.filter(join_model.permissao == (permissao.lower() == 'true'))

        if status:
            query = query.filter(join_model.status == (status.lower() == 'true'))

        return query

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro na aplicação dos filtros de responsáveis por filial: {e}")
        return db.session.query(model)
