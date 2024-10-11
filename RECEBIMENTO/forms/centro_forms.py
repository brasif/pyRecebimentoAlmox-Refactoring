from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class CentroForm(FlaskForm):
    # Nome do centro
    nome_centro = StringField('Nome do Centro (número)', validators=[
        DataRequired(message="O nome do centro é obrigatório."),
        Length(min=2, max=4),
        Regexp('^\d{1,4}$', message="O nome do centro deve ser um número inteiro.")
    ])
    
    # Campo para selecionar o a filial
    filial = SelectField('Filial', choices=[], validators=[
        DataRequired(message="Por favor, selecione uma filial.")
    ])
    
    submit = SubmitField('Salvar')
