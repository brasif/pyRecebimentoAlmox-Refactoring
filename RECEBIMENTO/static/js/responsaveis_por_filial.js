$(document).ready(function () {
    // Quando a filial é selecionada, buscar os responsáveis associados
    $('#filial-select').change(function () {
        var filial_name = $(this).val();

        if (filial_name && filial_name !== "") {
            // Realiza a chamada AJAX para buscar os responsáveis associados
            $.ajax({
                url: "/nota_fiscal/get_responsaveis",
                type: 'GET',
                data: { filial: filial_name },
                success: function (data) {
                    // Limpa o dropdown de responsáveis
                    $('#id_responsavel-select').empty().prop('disabled', false);

                    // Verifica se há responsáveis retornados
                    if (data.error) {
                        alert(data.error); // Exibe um alerta caso haja erro
                    } else {
                        // Adiciona uma opção padrão
                        $('#id_responsavel-select').append('<option value="">Selecione um responsável</option>');

                        // Atualiza o dropdown de responsáveis com as opções retornadas
                        data.forEach(function (responsavel) {
                            $('#id_responsavel-select').append(`<option value="${responsavel.value}">${responsavel.label}</option>`);
                        });
                    }
                },
                error: function () {
                    alert("Erro ao carregar responsáveis.");
                }
            });
        } else {
            $('#id_responsavel-select').prop('disabled', true).empty(); // Limpa o dropdown se não houver filial
        }
    });
});
