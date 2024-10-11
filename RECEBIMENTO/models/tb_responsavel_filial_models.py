from RECEBIMENTO import db
from datetime import datetime
from .enum_filiais import Filiais


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
        return f"<ResponsavelFilial - Responsavel: {self.id_responsavel} - Filial: {self.filial}>"


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
