$(function() {

    var currentURL = new URL(window.location.href);     
    var queries = currentURL.search;
    var parameters = new URLSearchParams(queries);

    //Page navigation
    $('#page-number').keyup(function(event) {        
        if (event.keyCode == '13') {
            if ($('#page-number')[0].checkValidity()) {
                var pageNumber = $('#page-number').val();
                /*
                parameters.set('page', pageNumber - 1);
                currentURL.search = parameters.toString();
                window.location.assign(currentURL.toString());
                */
                window.location.search = jQuery.query.set("page", pageNumber - 1);
            } else {
                $('#page-number')[0].reportValidity();
            }         
        }
    });

    $('#next-page-button').click(function() {
        /*
        parameters.set('page', currentPageNumber + 1);
        currentURL.search = parameters.toString();
        window.location.assign(currentURL.toString());
        */        
        window.location.search = jQuery.query.set("page", currentPageNumber + 1);
    });

    $('#prev-page-button').click(function() {
        /*
        parameters.set('page', currentPageNumber - 1);
        currentURL.search = parameters.toString();
        window.location.assign(currentURL.toString());
        */
       window.location.search = jQuery.query.set("page", currentPageNumber - 1);
    });
});