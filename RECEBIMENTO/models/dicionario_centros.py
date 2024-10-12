from .enum_filiais import Filiais

# Dicionário para relacionar centros às suas respectivas filiais
CENTROS_POR_FILIAL = {
    Filiais.JUNDIAI: ["0136", "1136"],
    Filiais.BELO_HORIZONTE: ["0184", "0103", "1101"],
    Filiais.RIO_DE_JANEIRO: ["0102", "1102"],
    Filiais.BRASILIA: ["0127", "1127"],
    Filiais.CURITIBA: ["1124"],
    Filiais.CUIABA: ["0185", "1125"],
    Filiais.RIBEIRAO_PRETO: ["0126"],
    Filiais.TOCANTINS: ["0157"],
    Filiais.GOIANIA: ["0121", "1121"],
    Filiais.ESPIRITO_SANTO: ["0120", "1120"]
}