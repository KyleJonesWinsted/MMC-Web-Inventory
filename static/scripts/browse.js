$(function() {

    function categorySearch() {
        var categoryString = $('#category-entry').val();
        var baseURL = "/browse/items?browse_type=Category&filter_id="
        request = $.get('/api/get_id', { search_string: categoryString.toLowerCase(), object_type: 'category'})
        request.done(function(data) {
            window.location.assign(baseURL + data)
        });
        request.fail(function() {
            alert("The entered category name does not exist.")
        });
    }

    function locationSearch() {
        var locationString = $('#location-entry').val();
        var baseURL = "/browse/items?browse_type=Location&filter_id="
        request = $.get('/api/get_id', {search_string: locationString.toLowerCase(), object_type: 'location'})
        request.done(function(data) {
            window.location.assign(baseURL + data);
        });
        request.fail(function() {
            alert("The entered location ID does not exist.");
        });
    }

    function manufacturerSearch() {
        var manufacturerString = $('#manufacturer-entry').val();
        var baseURL = "/browse/items?browse_type=Manufacturer&filter_id="
        window.location.assign(baseURL + encodeURI(manufacturerString.toLowerCase()));
    }

    function itemSearch() {
        var itemSKU = $('#sku-entry').val();
        var baseURL = "/item/";
        window.location.assign(baseURL + encodeURI(itemSKU));
    }

    $('#category-submit').click(function() {
        categorySearch();
    });

    $('#category-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            categorySearch();
        }
    });

    $('#location-submit').click(function() {
        locationSearch();
    });

    $('#location-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            locationSearch();
        }
    });

    $('#manufacturer-submit').click(function() {
        manufacturerSearch();
    });

    $('#manufacturer-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            manufacturerSearch();
        }
    });

    $('#sku-submit').click(function() {
        itemSearch();
    });

    $('#sku-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            itemSearch();
        }
    });

});