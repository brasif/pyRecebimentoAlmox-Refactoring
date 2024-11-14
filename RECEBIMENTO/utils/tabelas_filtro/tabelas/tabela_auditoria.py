from RECEBIMENTO import db
from sqlalchemy import func


# Filtro da auditoria
def auditoria_filtro(model, acao, tabela_referenciada, coluna_alterada, id_responsavel, data_evento):

    # Consulta base para trazer os registros
    query = db.session.query(model)

    # Aplica filtro da ação se presente
    if acao:
        query = query.filter(model.acao.ilike(f'%{acao}%'))
    
    # Aplica filtro da tabela referenciada se presente
    if tabela_referenciada:
        query = query.filter(model.tabela_referenciada.ilike(f'%{tabela_referenciada}%'))
    
    # Aplica filtro da coluna alterada se presente
    if coluna_alterada:
        query = query.filter(model.coluna_alterada.ilike(f'%{coluna_alterada}%'))
    
    # Aplica filtro do id_responsavel se presente
    if id_responsavel:
        query = query.filter(model.id_responsavel == id_responsavel)
    
    # Aplica filtro da data do evento se presente
    if data_evento:
        query = query.filter(func.date(model.data_evento) == data_evento)
    
    return query
