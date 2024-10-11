from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp
from RECEBIMENTO.models import Filiais

class CentroForm(FlaskForm):
    # Nome do centro
    nome_centro = StringField('Nome do Centro (número)', validators=[
        DataRequired(message="O nome do centro é obrigatório."),
        Length(min=2, max=4),
        Regexp('^\d{1,4}$', message="O nome do centro deve ser um número inteiro.")
    ])
    
    # Filial
    filial = SelectField('Filial', choices=[(filial.name, filial.value) for filial in Filiais], validators=[
        DataRequired(message="A filial é obrigatória.")
    ])
    
    submit = SubmitField('Salvar')
