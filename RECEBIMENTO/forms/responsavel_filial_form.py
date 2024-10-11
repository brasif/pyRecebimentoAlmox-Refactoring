from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class ResponsavelFilialForm(FlaskForm):
    # Campo para selecionar o ID do responsável
    id_responsavel = SelectField('Responsável', coerce=int, validators=[
        DataRequired(message="Por favor, selecione um responsável.")
    ])
    
    # Campo para selecionar o a filial
    filial = SelectField('Filial', choices=[], validators=[
        DataRequired(message="Por favor, selecione uma filial.")
    ])
    
    submit = SubmitField('Vincular')
