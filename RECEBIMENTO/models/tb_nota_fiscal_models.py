from RECEBIMENTO import db
from datetime import datetime
from .enum_filiais import Filiais


class NotaFiscal(db.Model):
    __tablename__ = 'tb_nota_fiscal'
    
    id_nota_fiscal = db.Column(db.Integer, primary_key=True)
    chave_acesso = db.Column(db.String(44), unique=True, nullable=False)
    codigo_cte = db.Column(db.String(20), nullable=True)
    volumes = db.Column(db.Integer, nullable=False)
    filial = db.Column(db.Enum(Filiais), nullable=False)
    nome_centro = db.Column(db.String(4), nullable=False)
    data_vinculacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_alteracao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    registros = db.relationship('Registro', back_populates='nota_fiscal')
    
    def __repr__(self):
        return f"<NotaFiscal {self.chave_acesso} - Filial: {self.filial} - Centro: {self.id_centro}>"


    @classmethod
    def criar_nota_fiscal(cls, form):
        # Verifica se a chave de acesso já existe
        if cls.query.filter_by(chave_acesso=form.chave_acesso.data).first():
            raise ValueError("A chave de acesso já foi cadastrada. Por favor, verifique e tente novamente.")
        
        # Cria e retorna uma nova instância de Nota Fiscal
        return cls(
            chave_acesso=form.chave_acesso.data,
            codigo_cte=form.codigo_cte.data,
            volumes=form.volumes.data,
            filial=form.filial.data,
            nome_centro=form.nome_centro.data
        )

    def atualizacao_nota_fiscal(self, form):
        # Verifica se o responsável já existe para a combinação de responsável e filial, exceto para o responsável atual
        nota_fiscal_existe = NotaFiscal.query.filter_by(id_responsavel=form.id_responsavel.data, filial=form.filial.data).first()

        if nota_fiscal_existe and nota_fiscal_existe.id_nota_fiscal != self.id_nota_fiscal:
            raise ValueError("A chave de acesso já foi cadastrada. Por favor, verifique e tente novamente.")

        # Atualiza os atributos da instância com os dados do formulário
        self.chave_acesso = form.chave_acesso.data,
        self.codigo_cte = form.codigo_cte.data,
        self.volumes = form.volumes.data,
        self.filial = form.filial.data,
        self.nome_centro = form.nome_centro.data

        return self
