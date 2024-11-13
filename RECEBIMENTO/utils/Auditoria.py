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
