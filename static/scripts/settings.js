$( function() {
    
    const skuTextBox = document.getElementById('sku-textbox');

    $('#background-cover').hide();
    $('#sku-entry-frame').hide();

    //Show sku entry
    $('#adjust-stock-button').click( function() {
        $('#background-cover').fadeIn("fast");
        $('#sku-entry-frame').fadeIn("fast");
        $('#sku-textbox').val('');
        $('#sku-textbox').focus();
        $('#sku-entry-error-text').hide();
    });

    //Hide sku entry
    $('#background-cover').click( function() {
        $('#background-cover').fadeOut("fast");
        $('#sku-entry-frame').fadeOut("fast");
    });

    //SKU entry submit
    function entrySubmit() {
        if (skuTextBox.validity.patternMismatch) {
            $('#sku-entry-error-text').show("fast");
        } else {
            const itemSKU = skuTextBox.value;
            var request = $.get('/api/get_item', {item_sku: itemSKU});
            request.done(function(result) {
                const baseURL = '/settings/adjust_stock?item_sku=';          
                window.location.assign(baseURL + itemSKU);
            });
            request.fail(function(jqXHR, textStatus, errorThrown) {
                $('#sku-entry-error-text').show("fast");
            });
        }
    }

    $('#sku-entry-submit').click( function() {
        entrySubmit();
    });

    skuTextBox.addEventListener('keyup', function(event) {
        if (event.keyCode === 13) {
            entrySubmit();
        }
    });
});