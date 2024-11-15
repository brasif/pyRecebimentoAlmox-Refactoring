from RECEBIMENTO import db
from sqlalchemy import func


# Filtro da auditoria
def auditoria_filtro(model, model_resp, acao, tabela_referenciada, coluna_alterada, responsavel, data_evento):
    
    try:
        # Consulta base para trazer os registros com um join em Responsavel
        query = db.session.query(model).join(model_resp, model.id_responsavel == model_resp.id_responsavel)

        # Aplica filtro da ação se presente
        if acao:
            query = query.filter(model.acao.ilike(f'%{acao}%'))
        
        # Aplica filtro da tabela referenciada se presente
        if tabela_referenciada:
            query = query.filter(model.tabela_referenciada.ilike(f'%{tabela_referenciada}%'))
        
        # Aplica filtro da coluna alterada se presente
        if coluna_alterada:
            query = query.filter(model.coluna_alterada.ilike(f'%{coluna_alterada}%'))
        
        # Aplica filtro pelo nome do responsável se presente
        if responsavel:
            query = query.filter(model_resp.nome_responsavel.ilike(f'%{responsavel}%'))
        
        # Aplica filtro da data do evento se presente
        if data_evento:
            query = query.filter(func.date(model.data_evento) == data_evento)
        
        return query

    except:
        raise ValueError("Erro ao aplicar filtros na auditoria. Verifique os parâmetros fornecidos.")
