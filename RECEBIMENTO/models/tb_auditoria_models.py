from RECEBIMENTO import db
from datetime import datetime


# Model
class Auditoria(db.Model):
    __tablename__ = 'tb_auditoria'

    id_auditoria = db.Column(db.Integer, primary_key=True)
    tabela_referenciada = db.Column(db.String(50), nullable=False)
    id_referencia = db.Column(db.Integer)
    acao = db.Column(db.String(50), nullable=False)
    coluna_alterada = db.Column(db.String(100))
    valor_antigo = db.Column(db.Text)
    valor_novo = db.Column(db.Text)
    id_responsavel = db.Column(db.Integer, db.ForeignKey('tb_responsavel.id_responsavel'))
    data_evento = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento
    responsavel = db.relationship('Responsavel', backref='auditorias')

    def __repr__(self):
        return (f"<Auditoria(id_auditoria={self.id_auditoria}, "
                f"tabela_referenciada='{self.tabela_referenciada}', "
                f"id_referencia={self.id_referencia}, "
                f"acao='{self.acao}', "
                f"coluna_alterada='{self.coluna_alterada}', "
                f"valor_antigo='{self.valor_antigo}', "
                f"valor_novo='{self.valor_novo}', "
                f"id_responsavel={self.id_responsavel}, "
                f"data_evento='{self.data_evento}')>")
