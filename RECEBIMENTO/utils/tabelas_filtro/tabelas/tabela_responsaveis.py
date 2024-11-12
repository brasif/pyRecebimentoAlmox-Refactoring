from RECEBIMENTO import db


# Filtro de responsáveis
def responsaveis_filtro(model, nome, email, permissao, status):

    # Consulta base para trazer os registros
    query = db.session.query(model)

    # Aplica filtro do nome se presente
    if nome:
        query = query.filter(model.nome_responsavel.ilike(f'%{nome}%'))
    
    # Aplica filtro do email se presente
    if email:
        query = query.filter(model.email.ilike(f'%{email}%'))

    # Aplica filtro de permissão se presente
    if permissao:
        query = query.filter(model.permissao == (permissao.lower() == 'true'))
    
    # Aplica filtro de status se presente
    if status:
        query = query.filter(model.status == (status.lower() == 'true'))
    
    return query
