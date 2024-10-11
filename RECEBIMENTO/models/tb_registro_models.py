from RECEBIMENTO import db
from datetime import datetime


class Registro(db.Model):
    __tablename__ = 'tb_registro'
    
    id_registro = db.Column(db.Integer, primary_key=True)
    id_nota_fiscal = db.Column(db.Integer, db.ForeignKey('tb_nota_fiscal.id_nota_fiscal'), nullable=False)
    data_recebimento = db.Column(db.DateTime, nullable=False)
    status_registro = db.Column(db.String(50), nullable=False)
    data_guarda = db.Column(db.DateTime)
    prioridade = db.Column(db.Boolean, default=False)
    id_responsavel = db.Column(db.Integer, db.ForeignKey('tb_responsavel.id_responsavel'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    nota_fiscal = db.relationship('NotaFiscal', back_populates='registros')
    responsavel = db.relationship('Responsavel', back_populates='registros')

    def __repr__(self):
        return f"<Registro {self.id_registro} - Nota Fiscal: {self.id_nota_fiscal} - Responsavel: {self.id_responsavel}>"
