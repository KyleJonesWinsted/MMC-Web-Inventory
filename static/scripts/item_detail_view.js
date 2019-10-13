$(function() {
    $('#stock-in-out-button').click( function() {     
        $('#stock-in-out-frame').css('display', 'block');
        $('#background-cover').css('display', 'block');
    });
    
    $('#background-cover').click( function() {
        $('#background-cover').css('display', 'none');
        $('#stock-in-out-frame').css('display', 'none');
    });
});