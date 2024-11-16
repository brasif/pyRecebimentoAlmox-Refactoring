from RECEBIMENTO import db
from sqlalchemy import func
import logging

# Configuração do logger
logging.basicConfig(level=logging.ERROR)


def notas_fiscais_filtro(model, **filtros):

    try:
        query = db.session.query(model)

        if filtros.get('chave_acesso'):
            query = query.filter(model.chave_acesso.ilike(f"%{filtros['chave_acesso']}%"))

        if filtros.get('nota_fiscal'):
            query = query.filter(func.substr(model.chave_acesso, 27, 34).ilike(f"%{filtros['nota_fiscal']}%"))

        if filtros.get('cnpj'):
            query = query.filter(func.substr(model.chave_acesso, 6, 20).ilike(f"%{filtros['cnpj']}%"))

        if filtros.get('filial'):
            query = query.filter(model.filial == f"%{filtros['filial']}%")

        if filtros.get('centro'):
            query = query.filter(model.nome_centro.ilike(f"%{filtros['centro']}%"))

        if filtros.get('prioridade'):
            query = query.filter(model.prioridade == (f"%{filtros['prioridade']}%".lower() == 'true'))

        return query

    except Exception as e:
        logging.error(f"Erro ao aplicar filtros nas notas fiscais: {e}")
        raise ValueError("Erro ao aplicar filtros nas notas fiscais.")
