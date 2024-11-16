from sqlalchemy import func, extract
import logging

# Configuração do logger
logging.basicConfig(level=logging.ERROR)


# Filtro de todos os registros por filial
def todos_registros_por_filial_filtro(model_nf, model_reg, model_resp, query, **filtros):

    try:
        # Filtro do mês
        if filtros.get('mes'):
            try:
                mes = int(filtros['mes'])  # Garantir que o mês seja um inteiro
                query = query.filter(extract('month', model_reg.data_recebimento) == mes)
            except ValueError:
                logging.logger.warning("Valor inválido para o mês: %s", filtros['mes'])

        # Filtro da chave de acesso
        if filtros.get('chave_acesso'):
            chave_acesso = f'%{filtros["chave_acesso"]}%'  # Preparar para comparação de substring
            query = query.filter(model_nf.chave_acesso.ilike(chave_acesso))

        # Filtro da nota fiscal
        if filtros.get('nota_fiscal'):
            nota_fiscal = f'%{filtros["nota_fiscal"]}%'  # Preparar para comparação de substring
            query = query.filter(func.substr(model_nf.chave_acesso, 27, 34).ilike(nota_fiscal))

        # Filtro do centro
        if filtros.get('centro'):
            centro = f'%{filtros["centro"]}%'  # Preparar para comparação de substring
            query = query.filter(model_nf.nome_centro.ilike(centro))

        # Filtro da prioridade
        if filtros.get('prioridade') is not None:
            query = query.filter(model_nf.prioridade == (filtros['prioridade'].lower() == 'true'))

        # Filtro do status do registro
        if filtros.get('status'):
            status = f'%{filtros["status"]}%'  # Preparar para comparação de substring
            query = query.filter(model_reg.status_registro.ilike(status))

        # Filtro do responsável
        if filtros.get('responsavel'):
            responsavel = f'%{filtros["responsavel"]}%'  # Preparar para comparação de substring
            query = query.filter(model_resp.nome_responsavel.ilike(responsavel))

        # Filtro da data de recebimento
        if filtros.get('data_recebimento'):
            try:
                data_recebimento = func.date(filtros['data_recebimento'])  # Converter para tipo date
                query = query.filter(func.date(model_reg.data_recebimento) == data_recebimento)
            except Exception:
                logging.logger.warning("Data de recebimento inválida: %s", filtros['data_recebimento'])

        # Filtro da data de guarda
        if filtros.get('data_guarda'):
            try:
                data_guarda = func.date(filtros['data_guarda'])  # Converter para tipo date
                query = query.filter(func.date(model_reg.data_guarda) == data_guarda)
            except Exception:
                logging.logger.warning("Data de guarda inválida: %s", filtros['data_guarda'])

        return query

    except Exception as e:
        logging.logger.error("Erro ao aplicar filtros nos registros por filial: %s", str(e))
        raise ValueError("Erro ao aplicar filtros nos registros por filial.")
