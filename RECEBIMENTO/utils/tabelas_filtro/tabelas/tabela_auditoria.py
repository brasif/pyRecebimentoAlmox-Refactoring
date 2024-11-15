from RECEBIMENTO import db
from sqlalchemy import func


# Filtro da auditoria
def auditoria_filtro(model, model_resp, **filtros):
    
    try:
        # Consulta base para trazer os registros com um join em Responsavel
        query = db.session.query(model).join(model_resp, model.id_responsavel == model_resp.id_responsavel)

        # Filtro da ação
        if filtros.get('acao'):
            query = query.filter(model.acao.ilike(f"%{filtros['acao']}%"))
        
        # Aplica filtro da tabela referenciada se presente
        if filtros.get('tabela_referenciada'):
            query = query.filter(model.tabela_referenciada.ilike(f"%{filtros['tabela_referenciada']}%"))
        
        # Aplica filtro da coluna alterada se presente
        if filtros.get('coluna_alterada'):
            query = query.filter(model.coluna_alterada.ilike(f"%{filtros['coluna_alterada']}%"))
        
        # Aplica filtro pelo nome do responsável se presente
        if filtros.get('responsavel'):
            query = query.filter(model_resp.nome_responsavel.ilike(f"%{filtros['responsavel']}%"))
        
        # Aplica filtro da data do evento se presente
        if filtros.get('data_evento'):
            query = query.filter(func.date(model.data_evento) == f"%{filtros['data_evento']}%")
        
        return query

    except:
        raise ValueError("Erro ao aplicar filtros na auditoria. Verifique os parâmetros fornecidos.")
