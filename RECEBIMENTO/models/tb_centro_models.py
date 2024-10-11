from RECEBIMENTO import db
from datetime import datetime
from .enum_filiais import Filiais


class Centro(db.Model):
    __tablename__ = 'tb_centro'
    
    id_centro = db.Column(db.Integer, primary_key=True)
    nome_centro = db.Column(db.String(4), unique=True, nullable=False)
    filial = db.Column(db.Enum(Filiais), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_alteracao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Centro {self.nome_centro} - Filial: {self.filial}>"
    
    
    @classmethod
    def criar_centro(cls, form):
        # Verifica se o centro já existe
        if cls.query.filter_by(nome_centro=form.nome_centro.data).first():
            raise ValueError(f"O centro '{form.nome_centro.data}' já existe. Por favor, escolha outro nome.")
        
        # Cria e retorna uma nova instância de Centro
        return cls(
            nome_centro=form.nome_centro.data,
            filial=form.filial.data
        )
    
    def atualizacao_centro(self, form):
        # Verifica se o centro já existe e é diferente do atual
        centro_existente = Centro.query.filter_by(nome_centro=form.nome_centro.data).first()

        if centro_existente and centro_existente.id_marca != self.id_marca:
            raise ValueError(f"O nome do centro '{form.nome_centro.data}' já está em uso por outro registro.")

        # Atualiza os atributos da instância com os dados do formulário
        self.nome_centro = form.nome_centro.data
        self.filial = form.filial.data

        return self
