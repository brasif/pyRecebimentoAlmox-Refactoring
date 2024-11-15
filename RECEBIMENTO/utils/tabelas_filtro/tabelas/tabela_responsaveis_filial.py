from RECEBIMENTO import db


# Filtro de responsáveis por filial
def responsaveis_filial_filtro(model, join_model, filial, nome, email, permissao, status):
    
    try:
        # Consulta base para trazer os responsáveis por filial e garantir o join com a tabela Responsavel
        query = db.session.query(model).join(join_model, model.id_responsavel == join_model.id_responsavel)

        # Aplica filtro de filial se presente
        if filial:
            query = query.filter(model.filial == filial)

        # Aplica filtro do nome se presente (na tabela Responsavel)
        if nome:
            query = query.filter(join_model.nome_responsavel.ilike(f'%{nome}%'))
        
        # Aplica filtro do email se presente (na tabela Responsavel)
        if email:
            query = query.filter(join_model.email.ilike(f'%{email}%'))

        # Aplica filtro de permissão se presente (na tabela Responsavel)
        if permissao:
            query = query.filter(join_model.permissao == (permissao.lower() == 'true'))
        
        # Aplica filtro de status se presente (na tabela Responsavel)
        if status:
            query = query.filter(join_model.status == (status.lower() == 'true'))
        
        return query

    except Exception as e:
        db.session.rollback()
        # Retorna consulta básica em caso de erro
        return db.session.query(model)
