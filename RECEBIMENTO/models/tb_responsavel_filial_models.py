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
