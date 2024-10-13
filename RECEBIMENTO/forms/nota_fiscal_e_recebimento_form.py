from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange


class NotaFiscalRecebimentoForm(FlaskForm):
    # Chave de acesso
    chave_acesso = StringField("Chave de acesso", validators=[
        DataRequired(message="A chave de acesso é obrigatória."),
        Length(min=44, max=44),
        Regexp(r'^\d{44,44}$', message="A chave de acesso deve ser composta apenas por números. (máximo 44 dígitos)")
    ])

    # Código CTE
    codigo_cte = StringField("Código CTE", validators=[
        Length(min=20, max=20),
        Regexp(r'^\d{20,20}$', message="A chave de acesso deve ser composta apenas por números. (máximo 20 dígitos)")
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

    # Prioridade (Sim/Não)
    prioridade = BooleanField("Prioridade", default=False)

    # Avaria (Sim/Não)
    avaria = BooleanField("Avaria", default=False)

    # Recusa (Sim/Não)
    recusa = BooleanField("Recusa", default=False)

    submit = SubmitField('Salvar')
