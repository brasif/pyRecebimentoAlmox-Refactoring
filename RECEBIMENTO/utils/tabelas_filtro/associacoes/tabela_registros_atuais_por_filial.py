from sqlalchemy import func, extract


# Filtro dos registros atuais por filial
def registros_atuais_por_filial_filtro(model_nf, model_reg, model_resp, query, mes, chave_acesso, nota_fiscal, centro, status, prioridade, responsavel, data_recebimento, data_guarda):
    
    # Filtro do mês
    if mes:
        query = query.filter(extract('month', model_reg.data_recebimento) == int(mes))

    # Filtro da chave de acesso
    if chave_acesso:
        query = query.filter(model_nf.chave_acesso.ilike(f'%{chave_acesso}%'))

    # Filtro da nota fiscal
    if nota_fiscal:
        query = query.filter(func.substr(model_nf.chave_acesso, 27, 34).ilike(f'%{nota_fiscal}%'))
    
    # Filtro do centro
    if centro:
        query = query.filter(model_nf.nome_centro.ilike(f'%{centro}%'))

    # Filtro da prioridade
    if prioridade:
        query = query.filter(model_nf.prioridade == (prioridade == 'true'))

    # Filtro do status do registro
    if status:
        query = query.filter(model_reg.status_registro.ilike(f'%{status}%'))

    # Filtro do responsável
    if responsavel:
        query = query.filter(model_resp.nome_responsavel.ilike(f'%{responsavel}%'))

    # Filtro da data de recebimento
    if data_recebimento:
        query = query.filter(func.date(model_reg.data_recebimento) == data_recebimento)

    # Filtro da data de guarda
    if data_guarda:
        query = query.filter(func.date(model_reg.data_guarda) == data_guarda)

    return query
