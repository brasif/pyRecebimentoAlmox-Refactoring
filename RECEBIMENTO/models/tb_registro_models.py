from RECEBIMENTO import db
from datetime import datetime
from babel.dates import format_date


class Registro(db.Model):
    __tablename__ = 'tb_registro'
    
    id_registro = db.Column(db.Integer, primary_key=True)
    id_nota_fiscal = db.Column(db.Integer, db.ForeignKey('tb_nota_fiscal.id_nota_fiscal'), nullable=False)
    data_recebimento = db.Column(db.DateTime, nullable=False)
    status_registro = db.Column(db.String(50), nullable=False)
    data_guarda = db.Column(db.DateTime)
    id_responsavel = db.Column(db.Integer, db.ForeignKey('tb_responsavel.id_responsavel'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    nota_fiscal = db.relationship('NotaFiscal', back_populates='registros')
    responsavel = db.relationship('Responsavel', back_populates='registros')

    def __repr__(self):
        return f"<Registro {self.id_registro} - Nota Fiscal: {self.id_nota_fiscal} - Responsavel: {self.id_responsavel}>"
    

    @property
    # Propriedade para extrair o nome do mês em portugês
    def mes(self):
        return format_date(self.data_recebimento, "MMMM", locale='pt_BR')


    @classmethod
    def criar_registro(cls, id_nota_fiscal, id_responsavel, status):
        # Verifica se a nota fiscal tem algum registro
        registro = cls.query.filter_by(id_nota_fiscal=id_nota_fiscal).first()
        if registro:
            data_recebimento = registro.data_recebimento
        else:
            data_recebimento = datetime.utcnow()

        # Verifica se o status é igual a "NF finalizada"
        if status == "NF finalizada":
            data_guarda = datetime.utcnow()
        else:
            data_guarda = None

        # Cria e retorna uma nova instância de registro
        return cls(
            id_nota_fiscal=id_nota_fiscal,
            data_recebimento=data_recebimento,
            status_registro=status,
            data_guarda=data_guarda,
            id_responsavel=id_responsavel
        )