$(function() {

    const apiURL = '/api/get_id';

    function createBaseURL(browseType) {
        return "/browse/items?browse_type=" + browseType + "&filter_id="
    }

    function categorySearch() {
        var categoryString = $('#category-entry').val();
        var baseURL = createBaseURL("Category");
        var request = $.get(apiURL, { search_string: categoryString.toLowerCase(), object_type: 'category'})
        request.done(function(data) {
            window.location.assign(baseURL + data)
        });
        request.fail(function() {
            alert("The entered category name does not exist.")
        });
    }

    function locationSearch() {
        var locationString = $('#location-entry').val();
        var baseURL = createBaseURL("Location");
        var request = $.get(apiURL, {search_string: locationString.toLowerCase(), object_type: 'location'})
        request.done(function(data) {
            window.location.assign(baseURL + data);
        });
        request.fail(function() {
            alert("The entered location ID does not exist.");
        });
    }

    function manufacturerSearch() {
        var manufacturerString = $('#manufacturer-entry').val();
        var baseURL = createBaseURL("Manufacturer");
        var request = $.get(apiURL, {search_string: manufacturerString.toLowerCase(), object_type: 'manufacturer'})
        request.done(function(data) {
            window.location.assign(baseURL + data);
        });
        request.fail(function() {
            alert("The entered manufacturer does not exist.");
        });
    }

    function itemSearch() {
        var itemSKU = $('#sku-entry').val();
        var baseURL = "/item/";
        var request = $.get(apiURL, {search_string: itemSKU, object_type: 'item'})
        request.done(function(data) {
            window.location.assign(baseURL + data)
        });
        request.fail(function() {
            alert("The entered SKU number does not exist.")
        });
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