from RECEBIMENTO import db
from sqlalchemy.orm import aliased
from sqlalchemy import func


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


# Filtro de notas fiscais
def notas_fiscais_filtro(model, chave_acesso, nota_fiscal, cnpj, filial, centro, prioridade):

    query = consulta_base(model)

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


# Filtro de todos os registros
def todos_registros_filtro(model_nf, model_reg, model_resp, query, chave_acesso, nota_fiscal, filial, centro, status, prioridade, responsavel):
    # Aplica filtro da chave de acesso se presente
    if chave_acesso:
        query = query.filter(model_nf.chave_acesso.ilike(f'%{chave_acesso}%'))

    # Filtro da nota fiscal se presente
    if nota_fiscal:
        # Aplica filtro utilizando a propriedade numero_nf
        query = query.filter(func.substr(model_nf.chave_acesso, 27, 34).ilike(f'%{nota_fiscal}%'))

    # Aplica filtro de filial se presente
    if filial:
        query = query.filter(model_nf.filial == filial)

    # Aplica filtro do centro se presente
    if centro:
        query = query.filter(model_nf.nome_centro.ilike(f'%{centro}%'))

    # Aplica filtro de prioridade se presente
    if prioridade:
        query = query.filter(model_nf.prioridade == (prioridade == 'true'))

    # Aplica filtro do status_registro se presente
    if status:
        query = query.filter(model_reg.status_registro.ilike(f'%{status}%'))

    # Aplica filtro do responsável pela atualização se presente
    if responsavel:
        query = query.filter(model_resp.nome_responsavel.ilike(f'%{responsavel}%'))

    return query