$( function() {

    function adjustStockSearch() {
        var itemSKU = $('#adjust-entry').val();
        var baseURL = '/settings/adjust_stock?item_sku=';
        var request = $.get('/api/get_id', {search_string: itemSKU, object_type: 'item'});
        request.done(function(data) {
            window.location.assign(baseURL + data);
        });
        request.fail(function() {
            alert("The entered SKU does not exist.");
        });
    }

    $('#adjust-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            adjustStockSearch();
        }
    });

    $('#adjust-submit').click(function() {
        adjustStockSearch();
    });
 
});