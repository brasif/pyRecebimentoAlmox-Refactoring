from RECEBIMENTO import db
from sqlalchemy import func, extract
import logging

# Configuração do logger
logging.basicConfig(level=logging.ERROR)


def todos_registros_filtro(model_reg, model_nf, model_resp, **filtros):
    
    try:
        query = db.session.query(model_reg).join(model_nf)

        if filtros.get('mes'):
            try:
                mes = int(filtros['mes'])
                query = query.filter(extract('month', model_reg.data_recebimento) == mes)
            except ValueError:
                logging.error("Filtro 'mes' inválido: não é um número.")
                pass

        if filtros.get('chave_acesso'):
            query = query.filter(model_nf.chave_acesso.ilike(f"%{filtros['chave_acesso']}%"))

        if filtros.get('nota_fiscal'):
            query = query.filter(func.substr(model_nf.chave_acesso, 27, 34).ilike(f"%{filtros['nota_fiscal']}%"))

        if filtros.get('filial'):
            query = query.filter(model_nf.filial == filtros['filial'])

        if filtros.get('centro'):
            query = query.filter(model_nf.nome_centro.ilike(f"%{filtros['centro']}%"))

        if filtros.get('prioridade') is not None:
            query = query.filter(model_nf.prioridade == (filtros['prioridade'].lower() == 'true'))

        if filtros.get('status'):
            query = query.filter(model_reg.status_registro.ilike(f"%{filtros['status']}%"))

        if filtros.get('responsavel'):
            query = query.join(model_resp).filter(model_resp.nome_responsavel.ilike(f"%{filtros['responsavel']}%"))

        if filtros.get('data_recebimento'):
            try:
                query = query.filter(func.date(model_reg.data_recebimento) == filtros['data_recebimento'])
            except ValueError:
                logging.error("Filtro 'data_recebimento' inválido.")
                pass

        if filtros.get('data_guarda'):
            try:
                query = query.filter(func.date(model_reg.data_guarda) == filtros['data_guarda'])
            except ValueError:
                logging.error("Filtro 'data_guarda' inválido.")
                pass

        return query

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro na aplicação dos filtros: {e}")
        return db.session.query(model_reg)
