from RECEBIMENTO import db
from sqlalchemy.orm import aliased


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
