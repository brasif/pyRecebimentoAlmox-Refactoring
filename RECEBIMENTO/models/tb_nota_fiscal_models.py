from RECEBIMENTO import db
from datetime import datetime
from .enum_filiais import Filiais
from sqlalchemy import event


# Model
class NotaFiscal(db.Model):
    __tablename__ = 'tb_nota_fiscal'
    
    id_nota_fiscal = db.Column(db.Integer, primary_key=True)
    chave_acesso = db.Column(db.String(44), unique=True, nullable=False)
    codigo_cte = db.Column(db.String(20))
    volumes = db.Column(db.Integer, nullable=False)
    filial = db.Column(db.Enum(Filiais), nullable=False)
    nome_centro = db.Column(db.String(4), nullable=False)
    prioridade = db.Column(db.Boolean, default=False)
    avaria = db.Column(db.Boolean, default=False)
    recusa = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_alteracao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    registros = db.relationship('Registro', back_populates='nota_fiscal')

    def __repr__(self):
        return (
            f"<NotaFiscal(id_nota_fiscal={self.id_nota_fiscal}, "
            f"chave_acesso='{self.chave_acesso}', "
            f"codigo_cte='{self.codigo_cte}', "
            f"volumes={self.volumes}, "
            f"filial='{self.filial.name}', "
            f"nome_centro='{self.nome_centro}', "
            f"prioridade={'Sim' if self.prioridade else 'Não'}, "
            f"avaria={'Sim' if self.avaria else 'Não'}, "
            f"recusa={'Sim' if self.recusa else 'Não'}, "
            f"data_criacao='{self.data_criacao}', "
            f"data_alteracao='{self.data_alteracao}')>"
        )


    @property
    # Propriedade para extrair CNPJ a partir da chave de acesso
    def cnpj(self):
        return str(self.chave_acesso[6:20])

    @property
    # Propriedade para extrair o número da NF da chave de acesso
    def numero_nf(self):
        return self.chave_acesso[27:34]


    @classmethod
    def criar_nota_fiscal(cls, chave_acesso, form):
        # Verifica se a chave de acesso já existe
        if cls.query.filter_by(chave_acesso=chave_acesso).first():
            raise ValueError("A chave de acesso já foi cadastrada. Por favor, verifique e tente novamente.")
        
        # Cria e retorna uma nova instância de Nota Fiscal
        return cls(
            chave_acesso=chave_acesso,
            codigo_cte=form.codigo_cte.data,
            volumes=form.volumes.data,
            filial=form.filial.data,
            nome_centro=form.nome_centro.data,
            prioridade=form.prioridade.data,
            avaria=form.avaria.data,
            recusa=form.recusa.data
        )

    def atualizacao_nota_fiscal(self, form):
        # Verifica se a chave de acesso já existe, exceto para a chave de acesso atual
        nota_fiscal_existe = NotaFiscal.query.filter_by(chave_acesso=form.chave_acesso.data).first()

        if nota_fiscal_existe and nota_fiscal_existe.id_nota_fiscal != self.id_nota_fiscal:
            raise ValueError("A chave de acesso já foi cadastrada. Por favor, verifique e tente novamente.")

        # Atualiza os atributos da instância com os dados do formulário
        self.chave_acesso = form.chave_acesso.data
        self.codigo_cte = form.codigo_cte.data
        self.volumes = form.volumes.data
        self.filial = form.filial.data
        self.nome_centro = form.nome_centro.data
        self.prioridade = form.prioridade.data
        self.avaria = form.avaria.data
        self.recusa = form.recusa.data
        
        return self


# === Auditoria ===

# Listener - INSERT
@event.listens_for(NotaFiscal, 'after_insert')
def after_insert_listener(mapper, connection, target):
    from RECEBIMENTO.utils import insert
    insert(NotaFiscal, connection, target)

# Listener - UPDATE
@event.listens_for(NotaFiscal, 'after_update')
def after_update_listener(mapper, connection, target):
    from RECEBIMENTO.utils import update
    state = db.inspect(target)
    update(NotaFiscal, connection, target, state)
