$( function() {

    function itemSkuSearch(itemSKU, baseURL) {
        var request = $.get('/api/get_id', {search_string: itemSKU, object_type: 'item'});
        request.done(function(data) {
            window.location.assign(baseURL + data);
        });
        request.fail(function() {
            alert("The entered SKU does not exist.");
        });
    }

    function loadAdjustStockView() {
        var itemSKU = $('#adjust-entry').val();
        var baseURL = '/settings/adjust_stock?item_sku=';
        itemSkuSearch(itemSKU, baseURL);
    }

    function loadModifyItemView() {
        var itemSKU = $('#modify-entry').val();
        var baseURL = '/settings/modify_item_details?item_sku=';
        itemSkuSearch(itemSKU, baseURL);
    }

    $('#adjust-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            loadAdjustStockView();
        }
    });

    $('#adjust-submit').click(function() {
        loadAdjustStockView();
    });

    $('#modify-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            loadModifyItemView();
        }
    });

    $('#modify-submit').click(function() {
        loadModifyItemView();
    });
 
});