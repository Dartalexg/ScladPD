$(document).ready(function() {
    var buttonCountProducts;
    $('.add').click(function() { // автозаполнение полей формы добавления записи о товаре
        var buttonCategory = $(this).attr('category');
        var buttonProduct = $(this).attr('product');
        var buttonDivision = $(this).attr('division');
        $('#divisionInput').val(buttonDivision);
        $('#categoryInput').val(buttonCategory);
        $('#productInput').val(buttonProduct);
    });
    //    $( "#addForm" ).on( "submit", function( event ) {       // ограничение на количество в форме добавления
    //        if( $('#countInput').val() > buttonCountProducts && $('operationInput').val() == -1){
    //            alert('значение не может быть больше '+ buttonCountProducts);
    //            event.preventDefault();
    //        }
    //    });
    $('#closeFormButton').click(function() { // сброс данных формы добавления записи о товаре при закрытии
        $('#addForm').reset();
    });
    $('.select-item-clear-button').on('click', function() { // снятие всех checkbox в выборе категории
        $(this).siblings('.dropdown-item').find('input:checkbox').prop('checked', false);
        return false;
    });
    var text = $("#copyright-date").text(); // изменение даты copyright в подвале
    var date = new Date();
    text = text.slice(0, text.length - 4);
    $("#copyright-date").text(text + date.getFullYear());
    $('#searchInput').on('keypress', function(e) { // отправка запроса по enter
        if (e.which == 13) {
            $('#mainSearchForm').submit();
        }
    });
    $('#searchInput').on('input click', function() { // кнопка очистки поля поиска
        if ($(this).val().length > 0) {
            $('#clearSearchInputButton').show();
        } else {
            $('#clearSearchInputButton').hide();
        }
    });
    if ($('#searchInput').val().length > 0) { // кнопка очистки поля поиска при загрузке страницы
        $('#clearSearchInputButton').show();
    } else {
        $('#clearSearchInputButton').hide();
    }
    $('#clearSearchInputButton').on('click', function() {
        $('#searchInput').val('');
        $('#clearSearchInputButton').hide();
    });

    $('input[name="dateRange"]').daterangepicker({
        autoUpdateInput: false,
        locale: {
            format: 'DD/MM/YYYY',
            cancelLabel: 'Clear'
        }
    });
    $('input[name="dateRange"]').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
        $('#mainSearchForm').trigger("submit");
    });
    $('input[name="dateRange"]').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
        $('#mainSearchForm').trigger("submit");
    });
    $('#addForm').submit(function(event) {
        event.preventDefault();

        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
//            url: '/consumption/',
            data: formData,
            success: function(data) {
                // Обработка успешного ответа
                location.reload();
            },
            error: function(xhr, textStatus, errorThrown) {
                if (xhr.status === 400) {
                    // Обработка ошибки (неверное количество товара)
                    alert('Ошибка ввода! Всего - ' + xhr.responseJSON.count + 'шт.')
                } else {
                    // Обработка других ошибок
                }
            }
        });
    });
});