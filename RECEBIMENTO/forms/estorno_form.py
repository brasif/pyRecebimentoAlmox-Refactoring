from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class EstornoForm(FlaskForm):
    # Campo para selecionar o ID do responsável
    id_responsavel = SelectField('Responsável', coerce=int, validators=[
        DataRequired(message="Por favor, selecione um responsável.")
    ])

    submit = SubmitField('Salvar')
