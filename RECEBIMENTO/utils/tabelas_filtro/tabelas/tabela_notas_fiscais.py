from RECEBIMENTO import db
from sqlalchemy import func


# Filtro de notas fiscais
def notas_fiscais_filtro(model, chave_acesso, nota_fiscal, cnpj, filial, centro, prioridade):
    
    try:
        # Consulta base para trazer os registros
        query = db.session.query(model)

        # Aplica filtro da chave de acesso se presente
        if chave_acesso:
            query = query.filter(model.chave_acesso.ilike(f'%{chave_acesso}%'))
        
        # Filtro da nota fiscal se presente
        if nota_fiscal:
            # Aplica o filtro sobre a substring específica da chave de acesso que corresponde ao número da NF
            query = query.filter(func.substr(model.chave_acesso, 27, 34).ilike(f'%{nota_fiscal}%'))
        
        # Aplica filtro do cnpj se presente
        if cnpj:
            # Aplica o filtro sobre a substring específica da chave de acesso que corresponde ao CNPJ
            query = query.filter(func.substr(model.chave_acesso, 6, 20).ilike(f'%{cnpj}%'))
        
        # Aplica filtro de filial se presente
        if filial:
            query = query.filter(model.filial == filial)
        
        # Aplica filtro do centro se presente
        if centro:
            query = query.filter(model.nome_centro.ilike(f'%{centro}%'))    
        
        # Aplica filtro de prioridade se presente
        if prioridade:
            query = query.filter(model.prioridade == (prioridade.lower() == 'true'))
        
        return query

    except:
        raise ValueError("Erro ao aplicar filtros nas notas fiscais.")
