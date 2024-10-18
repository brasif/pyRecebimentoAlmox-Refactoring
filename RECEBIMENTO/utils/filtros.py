from RECEBIMENTO import db
from sqlalchemy.orm import aliased


# Obtem a consulta base
def consulta_base(model):

    # Consulta base para trazer os registros
    query = db.session.query(model)
    
    return query


# ========== Filtros realizados a partir do HTML ==========

# Filtro de responsáveis
def responsaveis_filtro(model, nome, email, permissao, status):

    # Consulta base para trazer os responsáveis
    query = consulta_base(model)

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


# Filtro de responsáveis por filial
def responsaveis_filial_filtro(model, join_model, filial, nome, email, permissao, status):
    # Consulta base para trazer os responsáveis por filial e garantir o join com a tabela Responsavel
    ResponsavelAlias = aliased(join_model)  # Usando alias para evitar ambiguidades
    query = db.session.query(model).join(ResponsavelAlias, model.id_responsavel == ResponsavelAlias.id_responsavel)

    # Aplica filtro de filial se presente
    if filial:
        query = query.filter(model.filial == filial)

    # Aplica filtro do nome se presente (na tabela Responsavel)
    if nome:
        query = query.filter(ResponsavelAlias.nome_responsavel.ilike(f'%{nome}%'))
    
    # Aplica filtro do email se presente (na tabela Responsavel)
    if email:
        query = query.filter(ResponsavelAlias.email.ilike(f'%{email}%'))

    # Aplica filtro de permissão se presente (na tabela Responsavel)
    if permissao:
        query = query.filter(ResponsavelAlias.permissao == (permissao.lower() == 'true'))
    
    # Aplica filtro de status se presente (na tabela Responsavel)
    if status:
        query = query.filter(ResponsavelAlias.status == (status.lower() == 'true'))
    
    return query