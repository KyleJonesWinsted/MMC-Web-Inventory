$(function() {

    function employeeSearch() {
        var employeeString = $('#employee-entry').val();
        var baseURL = "/adjustments/adjustments?browse_type=employee&filter_id=";
        window.location.assign(baseURL + encodeURI(employeeString));
    }

    function dateSearch() {
        var dateString = $('#date-entry').val();
        var baseURL = "/adjustments/adjustments?browse_type=date&filter_id=";
        window.location.assign(baseURL + encodeURI(dateString));
    }

    function itemSearch() {
        var itemString = $('#sku-entry').val();
        var baseURL = "/adjustments/adjustments?browse_type=item&filter_id=";
        window.location.assign(baseURL + encodeURI(itemString));
    }

    function reasonSearch() {
        var reasonString = $('#reason-entry').val();
        var baseURL = "/adjustments/adjustments?browse_type=reason&filter_id=";
        request = $.get('/api/get_id', {search_string: reasonString.toLowerCase(), object_type: 'reason'});
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