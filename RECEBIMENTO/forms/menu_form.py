from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp


class ChaveAcessoForm(FlaskForm):
    # Chave de acesso
    chave_acesso = StringField("Chave de acesso", validators=[
        DataRequired(message="A chave de acesso é obrigatória."),
        Length(min=44, max=44),
        Regexp(r'^\d{44,44}$', message="A chave de acesso deve ser composta apenas por números. (máximo 44 dígitos)")
    ])