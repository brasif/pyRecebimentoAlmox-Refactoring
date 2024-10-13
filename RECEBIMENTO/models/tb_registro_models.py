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
    avaria = db.Column(db.Boolean, default=False)
    recusa = db.Column(db.Boolean, default=False)
    id_responsavel = db.Column(db.Integer, db.ForeignKey('tb_responsavel.id_responsavel'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    nota_fiscal = db.relationship('NotaFiscal', back_populates='registros')
    responsavel = db.relationship('Responsavel', back_populates='registros')

    def __repr__(self):
        return f"<Registro {self.id_registro} - Nota Fiscal: {self.id_nota_fiscal} - Responsavel: {self.id_responsavel}>"


    @classmethod
    def criar_registro(cls, id_responsavel, form):
        # Verifica se a nota fiscal tem algum registro
        if not cls.query.filter_by(id_nota_fiscal=form.id_nota_fiscal.data).first():
            data_recebimento = datetime.utcnow

        # Verifica se o status é igual a "NF finalizada"
        if form.status_registro.data == "NF finalizada":
            data_guarda = datetime.utcnow

        # Cria e retorna uma nova instância de registro
        return cls(
            id_nota_fiscal=form.id_nota_fiscal.data,
            data_recebimento=data_recebimento,
            status_registro=form.status_registro.data,
            data_guarda=data_guarda,
            prioridade=form.prioridade.data,
            avaria=form.avaria.data,
            recusa=form.recusa.data,
            id_responsavel=id_responsavel
        )