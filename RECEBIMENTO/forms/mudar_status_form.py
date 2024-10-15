from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class MudarStatusForm(FlaskForm):
    # Campo para selecionar o ID do responsável
    id_responsavel = SelectField('Responsável', coerce=int, validators=[
        DataRequired(message="Por favor, selecione um responsável.")
    ])
    
    # Status
    status = SelectField('Status', choices=[], validators=[
        DataRequired(message="Por favor, selecione um status.")
    ])

    submit = SubmitField('Salvar')
