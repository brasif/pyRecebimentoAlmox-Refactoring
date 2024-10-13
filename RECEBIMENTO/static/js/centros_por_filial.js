$(document).ready(function () {
    // Quando a filial é selecionada, buscar os centros associados
    $('#filial-select').change(function () {
        var filial_name = $(this).val();

        if (filial_name && filial_name !== "") {
            // Realiza a chamada AJAX para buscar os centros associados
            $.ajax({
                url: "/nota_fiscal/get_centros",
                type: 'GET',
                data: { filial: filial_name },
                success: function (data) {
                    // Limpa o dropdown de centros
                    $('#centro-select').empty().prop('disabled', false);

                    // Verifica se há centros retornados
                    if (data.error) {
                        alert(data.error); // Exibe um alerta caso haja erro
                    } else {
                        // Adiciona uma opção padrão
                        $('#centro-select').append('<option value="">Selecione um centro</option>');
                        
                        // Atualiza o dropdown de centros com as opções retornadas
                        data.forEach(function (centro) {
                            $('#centro-select').append(`<option value="${centro.value}">${centro.label}</option>`);
                        });
                    }
                },
                error: function () {
                    alert("Erro ao carregar centros.");
                }
            });
        } else {
            $('#centro-select').prop('disabled', true).empty(); // Limpa o dropdown se não houver filial
        }
    });
});
