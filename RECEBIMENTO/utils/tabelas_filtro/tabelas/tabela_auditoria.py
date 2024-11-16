from RECEBIMENTO import db
from sqlalchemy import func
import logging

# Configuração do logger
logging.basicConfig(level=logging.ERROR)


def auditoria_filtro(model, model_resp, **filtros):

    try:
        query = db.session.query(model).join(model_resp, model.id_responsavel == model_resp.id_responsavel)

        if filtros.get('acao'):
            query = query.filter(model.acao.ilike(f"%{filtros['acao']}%"))

        if filtros.get('tabela_referenciada'):
            query = query.filter(model.tabela_referenciada.ilike(f"%{filtros['tabela_referenciada']}%"))

        if filtros.get('coluna_alterada'):
            query = query.filter(model.coluna_alterada.ilike(f"%{filtros['coluna_alterada']}%"))

        if filtros.get('responsavel'):
            query = query.filter(model_resp.nome_responsavel.ilike(f"%{filtros['responsavel']}%"))

        if filtros.get('data_evento'):
            query = query.filter(func.date(model.data_evento) == f"%{filtros['data_evento']}%")

        return query

    except Exception as e:
        logging.error(f"Erro ao aplicar filtros na auditoria: {e}")
        raise ValueError("Erro ao aplicar filtros na auditoria.")
