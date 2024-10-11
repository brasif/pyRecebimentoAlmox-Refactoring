from RECEBIMENTO import db
from datetime import datetime
from .enum_filiais import Filiais


class NotaFiscal(db.Model):
    __tablename__ = 'tb_nota_fiscal'
    
    id_nota_fiscal = db.Column(db.Integer, primary_key=True)
    chave_acesso = db.Column(db.String(44), unique=True, nullable=False)
    CNPJ = db.Column(db.String(14), nullable=False)
    numero_nfe = db.Column(db.String(6), nullable=False)
    codigo_cte = db.Column(db.String(20), nullable=False)
    volumes = db.Column(db.Integer, nullable=False)
    filial = db.Column(db.Enum(Filiais), nullable=False)
    id_centro = db.Column(db.Integer, db.ForeignKey('tb_centro.id_centro'), nullable=False)
    data_vinculacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_alteracao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    registros = db.relationship('Registro', back_populates='nota_fiscal')

    def __repr__(self):
        return f"<NotaFiscal {self.chave_acesso} - Filial: {self.filial} - Centro: {self.id_centro}>"
