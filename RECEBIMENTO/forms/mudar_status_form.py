from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class MudarStatusForm(FlaskForm):
    # Status
    status = SelectField('Status', choices=[], validators=[
        DataRequired(message="Por favor, selecione um status.")
    ])

    submit = SubmitField('Salvar')
