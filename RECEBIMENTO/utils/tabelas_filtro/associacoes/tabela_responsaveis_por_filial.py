# Filtro de responsáveis por filial
def responsaveis_por_filial_filtro(model, query, nome, email, permissao, status):
    
    try:
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

    except:
        raise ValueError("Erro ao aplicar filtros nos registros por filial.")
