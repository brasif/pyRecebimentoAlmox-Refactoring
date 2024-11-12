from RECEBIMENTO import db
from datetime import datetime
from .enum_filiais import Filiais

# Importações para os enventos listeners
from sqlalchemy import event
from RECEBIMENTO.models.tb_auditoria import Auditoria
from sqlalchemy.orm import sessionmaker


class ResponsavelFilial(db.Model):
    __tablename__ = 'tb_responsavel_filial'
    
    id_responsavel_filial = db.Column(db.Integer, primary_key=True)
    id_responsavel = db.Column(db.Integer, db.ForeignKey('tb_responsavel.id_responsavel'), nullable=False)
    filial = db.Column(db.Enum(Filiais), nullable=False)
    data_vinculacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_alteracao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento
    responsavel = db.relationship('Responsavel', back_populates='responsavel_filial')

    def __repr__(self):
        return (f"<ResponsavelFilial(id_responsavel_filial={self.id_responsavel_filial}, "
                f"responsavel_id={self.id_responsavel}, "
                f"filial='{self.filial}', "
                f"data_vinculacao={self.data_vinculacao}, "
                f"data_alteracao={self.data_alteracao})>")

    @classmethod
    def criar_responsavel_filial(cls, form):
        # Verifica se o responsável já existe para a combinação de responsável e filial
        if cls.query.filter_by(id_responsavel=form.id_responsavel.data, filial=form.filial.data).first():
            raise ValueError("Já existe um responsável cadastrado para esta filial com os dados fornecidos. Por favor, verifique e tente novamente.")
        
        # Cria e retorna uma nova instância de Responsável
        return cls(
            id_responsavel=form.id_responsavel.data,
            filial=form.filial.data
        )
    
    def atualizacao_responsavel_filial(self, form):
        # Verifica se o responsável já existe para a combinação de responsável e filial, exceto para o responsável atual
        responsavel_filial_existente = ResponsavelFilial.query.filter_by(id_responsavel=form.id_responsavel.data, filial=form.filial.data).first()

        if responsavel_filial_existente and responsavel_filial_existente.id_responsavel_filial != self.id_responsavel_filial:
            raise ValueError("Já existe um responsável cadastrado para esta filial com os dados fornecidos. Por favor, verifique e tente novamente.")

        # Atualiza os atributos da instância com os dados do formulário
        self.id_responsavel = form.id_responsavel.data
        self.filial = form.filial.data

        return self


# listener - INSERT
@event.listens_for(ResponsavelFilial, 'after_insert')
def after_insert_listener(mapper, connection, target):
    session = sessionmaker(bind=connection)()
    
    # Registra a auditoria de criação
    auditoria = Auditoria(
        tabela_referenciada=ResponsavelFilial.__tablename__,
        id_referencia=target.id_responsavel_filial,
        acao="INSERT",
        coluna_alterada="Todos os campos",
        valor_antigo="Nenhum",
        valor_novo=f"id_responsavel: {target.id_responsavel}, "
                   f"filial: {target.filial}, "
                   f"data_vinculacao: {target.data_vinculacao}, "
                   f"data_alteracao: {target.data_alteracao}",
        id_responsavel=target.id_responsavel
    )
    
    session.add(auditoria)
    session.commit()

# listener - UPDATE
@event.listens_for(ResponsavelFilial, 'after_update')
def after_update_listener(mapper, connection, target):
    session = sessionmaker(bind=connection)()
    changes = []

    # Captura valores antigos e novos para colunas monitoradas
    if target.id_responsavel != target.__dict__.get('_original_id_responsavel', target.id_responsavel):
        changes.append(('id_responsavel', target.__dict__.get('_original_id_responsavel'), target.id_responsavel))
    
    if target.filial != target.__dict__.get('_original_filial', target.filial):
        changes.append(('filial', target.__dict__.get('_original_filial'), target.filial))

    for coluna, valor_antigo, valor_novo in changes:
        auditoria = Auditoria(
            tabela_referenciada=ResponsavelFilial.__tablename__,
            id_referencia=target.id_responsavel_filial,
            acao="UPDATE",
            coluna_alterada=coluna,
            valor_antigo=str(valor_antigo),
            valor_novo=str(valor_novo),
            id_responsavel=target.id_responsavel
        )
        session.add(auditoria)

    session.commit()

# listener - DELETE
@event.listens_for(ResponsavelFilial, 'load')
def load_original_state(target, context):
    target._original_id_responsavel = target.id_responsavel
    target._original_filial = target.filial


@event.listens_for(ResponsavelFilial, 'after_delete')
def after_delete_listener(mapper, connection, target):
    print(f"Responsável deletado: {target}")

    # Cria uma nova sessão para a auditoria
    Session = sessionmaker(bind=connection)
    session = Session()

    try:
        # Registra as informações antigas na auditoria
        auditoria = Auditoria(
            tabela_referenciada=ResponsavelFilial.__tablename__,
            id_referencia=target.id_responsavel_filial,
            acao="DELETE",
            id_responsavel=target.id_responsavel,
            coluna_alterada="Todos os campos",
            valor_antigo=f"id_responsavel: {target.id_responsavel}, "
                         f"filial: {target.filial}, "
                         f"data_vinculacao: {target.data_vinculacao}, "
                         f"data_alteracao: {target.data_alteracao}",
            valor_novo="Registro excluído"
        )

        session.add(auditoria)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erro ao salvar auditoria: {e}")
    finally:
        session.close()
