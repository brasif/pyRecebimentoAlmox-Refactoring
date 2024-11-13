from RECEBIMENTO.models.tb_auditoria_models import Auditoria
from sqlalchemy.orm import sessionmaker


def insert(model, connection, target):
    session = sessionmaker(bind=connection)()

    try:
        # Obtém o valor da chave primária (supondo que há apenas uma chave primária)
        primary_key_column = list(model.__table__.primary_key.columns)[0].name
        id_referencia = getattr(target, primary_key_column)

        # Constrói a string 'valor_novo' com base nos atributos do objeto
        valor_novo = ', '.join(f"{coluna}: {getattr(target, coluna)}" for coluna in target.__table__.columns.keys())

        auditoria = Auditoria(
            tabela_referenciada=model.__tablename__,
            id_referencia=id_referencia,
            acao="INSERT",
            coluna_alterada="Todos os campos",
            valor_antigo="Nenhum",
            valor_novo=valor_novo,
            id_responsavel=target.id_responsavel
        )

        session.add(auditoria)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erro ao salvar auditoria: {e}")
    finally:
        session.close()


def update(model, connection, target, state):
    session = sessionmaker(bind=connection)()
    changes = []

    # Verifica as alterações para os atributos que precisam ser auditados
    for attr in state.attrs:
        history = attr.load_history()
        if history.has_changes():
            coluna = attr.key
            valor_antigo = history.deleted[0] if history.deleted else None
            valor_novo = history.added[0] if history.added else None
            changes.append((coluna, valor_antigo, valor_novo))

    try:

        # Obtém o valor da chave primária (supondo que há apenas uma chave primária)
        primary_key_column = list(model.__table__.primary_key.columns)[0].name
        id_referencia = getattr(target, primary_key_column)

        for coluna, valor_antigo, valor_novo in changes:
            auditoria = Auditoria(
                tabela_referenciada=model.__tablename__,
                id_referencia=id_referencia,
                acao="UPDATE",
                coluna_alterada=coluna,
                valor_antigo=str(valor_antigo),
                valor_novo=str(valor_novo),
                id_responsavel=target.id_responsavel
            )
            session.add(auditoria)
        
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erro ao salvar auditoria: {e}")
    finally:
        session.close()


def delete(model, connection, target):

    # Cria uma nova sessão para a auditoria
    Session = sessionmaker(bind=connection)
    session = Session()

    try:

        # Obtém o valor da chave primária (supondo que há apenas uma chave primária)
        primary_key_column = list(model.__table__.primary_key.columns)[0].name
        id_referencia = getattr(target, primary_key_column)

        # Constrói a string 'valor_novo' com base nos atributos do objeto
        valor_antigo = ', '.join(f"{coluna}: {getattr(target, coluna)}" for coluna in target.__table__.columns.keys())

        # Registra as informações antigas na auditoria
        auditoria = Auditoria(
            tabela_referenciada=model.__tablename__,
            id_referencia=id_referencia,
            acao="DELETE",
            coluna_alterada="Todos os campos",
            valor_antigo=valor_antigo,
            valor_novo="Registro excluído",
            id_responsavel=target.id_responsavel
        )

        session.add(auditoria)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erro ao salvar auditoria: {e}")
    finally:
        session.close()
