from flask import flash
from sqlalchemy import func, extract


# Filtro dos registros atuais
def registros_atuais_filtro(model_nf, model_reg, model_resp, query, **filtros):
    
    try:
        # Filtro do mês
        if filtros.get('mes'):
            try:
                mes = int(filtros['mes'])
                query = query.filter(extract('month', model_reg.data_recebimento) == mes)
            except ValueError:
                flash("Não foi possível filtrar o mês")
                pass

        # Filtro da chave de acesso
        if filtros.get('chave_acesso'):
            query = query.filter(model_nf.chave_acesso.ilike(f"%{filtros['chave_acesso']}%"))

        # Filtro da nota fiscal
        if filtros.get('nota_fiscal'):
            query = query.filter(func.substr(model_nf.chave_acesso, 27, 34).ilike(f"%{filtros['nota_fiscal']}%"))

        # Filtro da filial
        if filtros.get('filial'):
            query = query.filter(model_nf.filial == filtros['filial'])

        # Filtro do centro
        if filtros.get('centro'):
            query = query.filter(model_nf.nome_centro.ilike(f"%{filtros['centro']}%"))

        # Filtro da prioridade
        if filtros.get('prioridade') is not None:
            query = query.filter(model_nf.prioridade == (filtros['prioridade'].lower() == 'true'))

        # Filtro do status do registro
        if filtros.get('status'):
            query = query.filter(model_reg.status_registro.ilike(f"%{filtros['status']}%"))

        # Filtro do responsável
        if filtros.get('responsavel'):
            query = query.join(model_resp).filter(model_resp.nome_responsavel.ilike(f"%{filtros['responsavel']}%"))

        # Filtro da dat de recebimento
        if filtros.get('data_recebimento'):
            try:
                query = query.filter(func.date(model_reg.data_recebimento) == filtros['data_recebimento'])
            except ValueError:
                flash("Data inválida")
                pass  # Ignora se a data não for válida

        # Filtro da data guarda
        if filtros.get('data_guarda'):
            try:
                query = query.filter(func.date(model_reg.data_guarda) == filtros['data_guarda'])
            except ValueError:
                flash("Data inválida")
                pass  # Ignora se a data não for válida

        return query

    except Exception as e:
        # Retorna a query sem filtros em caso de erro
        return query
