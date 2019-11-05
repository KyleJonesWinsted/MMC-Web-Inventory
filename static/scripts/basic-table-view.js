$(function() {

    var currentURL = new URL(window.location.href);     
    var queries = currentURL.search;
    var parameters = new URLSearchParams(queries);

    //Page navigation
    $('#page-number').keyup(function(event) {        
        if (event.keyCode == '13') {
            var pageNumber = $('#page-number').val();
            parameters.set('page', pageNumber - 1);
            currentURL.search = parameters.toString();
            window.location.assign(currentURL.toString());            
        }
    });

    $('#next-page-button').click(function() {
        parameters.set('page', currentPageNumber + 1);
        currentURL.search = parameters.toString();
        window.location.assign(currentURL.toString());
    });

    $('#prev-page-button').click(function() {
        parameters.set('page', currentPageNumber - 1);
        currentURL.search = parameters.toString();
        window.location.assign(currentURL.toString());
    });
});