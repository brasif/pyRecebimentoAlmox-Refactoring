from RECEBIMENTO import db
from sqlalchemy import func


# Filtro de notas fiscais
def notas_fiscais_filtro(model, **filtros):
    
    try:
        # Consulta base para trazer as notas fiscais
        query = db.session.query(model)

        # Filtro da chave de acesso
        if filtros.get('chave_acesso'):
            query = query.filter(model.chave_acesso.ilike(f"%{filtros['chave_acesso']}%"))
        
        # Filtro da nota fiscal
        if filtros.get('nota_fiscal'):
            query = query.filter(func.substr(model.chave_acesso, 27, 34).ilike(f"%{filtros['nota_fiscal']}%"))

        # Aplica filtro do cnpj
        if filtros.get('cnpj'):
            query = query.filter(func.substr(model.chave_acesso, 6, 20).ilike(f"%{filtros['cnpj']}%"))
        
        # Aplica filtro de filial
        if filtros.get('filial'):
            query = query.filter(model.filial == f"%{filtros['filial']}%")
        
        # Aplica filtro do centro
        if filtros.get('centro'):
            query = query.filter(model.nome_centro.ilike(f"%{filtros['centro']}%"))

        # Aplica filtro de prioridade
        if filtros.get('prioridade'):
            query = query.filter(model.prioridade == (f"%{filtros['prioridade']}%".lower() == 'true'))
        
        return query

    except:
        raise ValueError("Erro ao aplicar filtros nas notas fiscais.")
