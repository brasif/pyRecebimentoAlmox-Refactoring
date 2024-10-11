from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


class ResponsavelForm(FlaskForm):
    # permissão (Administrador/Usuário)
    permissao = BooleanField("Permissão", default=False)

    # Status (Ativo/Inativo)
    status = BooleanField("Ativo", default=True)
    
    submit = SubmitField('Salvar')
