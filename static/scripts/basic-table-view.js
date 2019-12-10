$(function() {
    //Page navigation

    function createUrlWithPage(page_number) {
        //Splits parameters from url, creates dict of parameters, modifies 'page' in dict and reattaches to url
        var url = window.location.href.toString();
        var splitURL = url.split("?");
        var modifiedURL = splitURL[0] + '?';
        var parameters = {};
        if (splitURL.length == 2) {
            var param_strings = splitURL[1].split("&");
            for (param_string of param_strings) {
                if (param_string != "") {                    
                    const keyRegex = new RegExp('(.+)\=');
                    const valueRegex = new RegExp('\=(.+)');
                    var key = param_string.match(keyRegex)[1];
                    var value = param_string.match(valueRegex)[1];
                    parameters[key] = value;
                }
            }
        }
        parameters['page'] = page_number;
        for (key in parameters) {
            modifiedURL += key + '=' + parameters[key] + '&';
        }        
        return modifiedURL;
    }

    $('#page-number').keyup(function(event) {        
        if (event.keyCode == '13') {
            if ($('#page-number')[0].checkValidity()) {
                var pageNumber = $('#page-number').val();
                window.location.assign(createUrlWithPage(pageNumber - 1));
            } else {
                $('#page-number')[0].reportValidity();
            }         
        }
    });

    $('#next-page-button').click(function() {
        window.location.assign(createUrlWithPage(currentPageNumber + 1));   
    });

    $('#prev-page-button').click(function() {
        window.location.assign(createUrlWithPage(currentPageNumber - 1));
    });
});