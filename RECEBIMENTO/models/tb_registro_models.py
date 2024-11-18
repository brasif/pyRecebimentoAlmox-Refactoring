from RECEBIMENTO import db
from datetime import datetime
from babel.dates import format_date


# Model
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
        return (
            f"<Registro(id_registro={self.id_registro}, "
            f"id_nota_fiscal={self.id_nota_fiscal}, "
            f"data_recebimento='{format_date(self.data_recebimento, format='short')}', "
            f"status_registro='{self.status_registro}', "
            f"data_guarda='{format_date(self.data_guarda, format='short') if self.data_guarda else 'Não Guardado'}', "
            f"id_responsavel={self.id_responsavel}, "
            f"data_criacao='{format_date(self.data_criacao, format='short')}')>"
        )


    @property
    # Propriedade para extrair o nome do mês em portugês
    def mes(self):
        return format_date(self.data_recebimento, "MMMM", locale='pt_BR')


    @classmethod
    def criar_registro(cls, id_nota_fiscal, id_responsavel, status):

        # Verifica se a nota fiscal tem algum registro
        registro = cls.query.filter_by(id_nota_fiscal=id_nota_fiscal).first()

        if registro and registro.status_registro != "Estornado":
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