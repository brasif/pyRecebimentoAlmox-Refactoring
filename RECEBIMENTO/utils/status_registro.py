# Dicionário - REGISTRO_STATUS_CHOICES
REGISTRO_STATUS_CHOICES = [
    ("Pendência almoxarifado", "Pendência almoxarifado"),
    ("Aguardando ajuste", "Aguardando ajuste"),
    ("Aguardando fiscal", "Aguardando fiscal"),
    ("Aguardando lançamento de CTE", "Aguardando lançamento de CTE"),
    ("NF cancelada", "NF cancelada"),
    ("NF finalizada", "NF finalizada")
]


# Função para gerar status incial em Recebimento
def definicao_status_recebimento(recusa, avaria):
    if recusa and avaria:
        status = "Recusado por avaria"
    elif recusa:
        status = "Recusa"
    else:
        status = "Aguardando Conferência"
    return status