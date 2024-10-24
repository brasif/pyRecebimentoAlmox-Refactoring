from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange


class NotaFiscalRecebimentoForm(FlaskForm):

    # Código CTE (opcional)
    codigo_cte = StringField("Código CTE", validators=[
        Length(min=0, max=20),
        Regexp(r'^\d{0,20}$', message="O código CTE deve ser composto apenas por números. (máximo 20 dígitos)")
    ])

    # Volumes
    volumes = IntegerField('Volumes', validators=[
        DataRequired(message="O volume é obrigatório."),
        NumberRange(min=1, max=1000, message="O volume deve ser um número inteiro entre 0 e 1.000")
    ])

    # Campo para selecionar a filial
    filial = SelectField('Filial', choices=[], validators=[
        DataRequired(message="Por favor, selecione uma filial.")
    ])

    # Campo para selecionar o centro
    nome_centro = SelectField('Centro', choices=[], validators=[
        DataRequired(message="Por favor, selecione um centro.")
    ])

    # Campo para selecionar o ID do responsável
    id_responsavel = SelectField('Responsável', coerce=int, validators=[
        DataRequired(message="Por favor, selecione um responsável.")
    ])

    # Prioridade (Sim/Não)
    prioridade = BooleanField("Prioridade", default=False)

    # Avaria (Sim/Não)
    avaria = BooleanField("Avaria", default=False)

    # Recusa (Sim/Não)
    recusa = BooleanField("Recusa", default=False)

    submit = SubmitField('Salvar')
