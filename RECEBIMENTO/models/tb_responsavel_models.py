from RECEBIMENTO import db
from datetime import datetime


class Responsavel(db.Model):
    __tablename__ = 'tb_responsavel'
    
    id_responsavel = db.Column(db.Integer, primary_key=True)
    nome_responsavel = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    id_azure_ad = db.Column(db.String(255), unique=True, nullable=False)
    permissao = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_alteracao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    registros = db.relationship('Registro', back_populates='responsavel')
    responsavel_filial = db.relationship('ResponsavelFilial', back_populates='responsavel')
    
    
    def __repr__(self):
        return f"<Responsavel {self.nome_responsavel} - Email: {self.email}>"
    
    # Propriedades exigidas pelo Flask-Login
    @property
    def is_active(self):
        # Verifica se o usuário está ativo
        return self.status

    @property
    def is_authenticated(self):
        # Verifica se o usuário está autenticado
        return True

    @property
    def is_anonymous(self):
        # Verifica se o usuário é anônimo
        return False

    def get_id(self):
        # Retorna o ID do usuário
        return str(self.id_responsavel)
    
    def atualizacao_responsavel(self, form):
        # Atualiza os atributos da instância com os dados do formulário
        self.permissao = form.permissao.data
        self.status = form.status.data

        return self
