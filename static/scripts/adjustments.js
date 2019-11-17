$(function() {

    const apiURL = "/api/get_id"

    function createBaseURL(browseType) {
        return "/adjustments/adjustments?browse_type=" + browseType + "&filter_id="
    }

    function employeeSearch() {
        var employeeString = $('#employee-entry').val();
        var baseURL = createBaseURL("employee");
        var request = $.get(apiURL, {search_string: employeeString, object_type: 'employee'});
        request.done(function(data) {
            window.location.assign(baseURL + data);
        });
        request.fail(function() {
            alert("The entered employee ID does not exist.");
        });
    }

    function dateSearch() {
        var dateString = $('#date-entry').val();
        var baseURL = createBaseURL("date");
        var dateTextbox = document.getElementById('date-entry');
        if (dateTextbox.validity.patternMismatch) {
            alert("Please enter a valid date.");
        } else {
            window.location.assign(baseURL + encodeURI(dateString));
        }
    }

    function itemSearch() {        
        var itemString = $('#sku-entry').val();
        var baseURL = createBaseURL("item");
        var request = $.get(apiURL, {search_string: itemString, object_type: 'item'});
        request.done(function(data) {
            window.location.assign(baseURL + data);
        });
        request.fail(function() {
            alert('The entered SKU number does not exist.');
        });
    }

    function reasonSearch() {
        var reasonString = $('#reason-entry').val();
        var baseURL = "/adjustments/adjustments?browse_type=reason&filter_id=";
        var request = $.get('/api/get_id', {search_string: reasonString.toLowerCase(), object_type: 'reason'});
        request.done(function(data) {
            window.location.assign(baseURL + data);
        });
        request.fail(function() {
            alert('The entered reason name does not exist.');
        });
    }

    $('#employee-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            employeeSearch();
        }
    });

    $('#date-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            dateSearch()
        }
    });

    $('#sku-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            itemSearch()
        }
    });

    $('#reason-entry').keyup(function(event) {
        if (event.keyCode == '13') {
            reasonSearch()
        }
    });

    $('#employee-submit').click(function() {
        employeeSearch()
    });

    $('#date-submit').click(function() {
        dateSearch()
    });

    $('#sku-submit').click(function() {
        itemSearch()
    });

    $('#reason-submit').click(function() {
        reasonSearch()
    });
});