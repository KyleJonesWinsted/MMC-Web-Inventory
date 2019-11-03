$(function() {

    //Add to picklist
    $('.add-to-picklist-button').click(function() {        
        var locationItemId = this.parentElement.id;
        $(this).attr('disabled', true);
        request = $.get('/api/add_item_to_picklist', {location_item_id: locationItemId});
        request.done(function() {
            $(this).attr('disabled', false);
            getPicklist();
        });
        request.fail(function() {
            $(this).attr('disabled', false);
            alert("An error occured. If there is no active picklist, please create a new one, or select one from the left sidebar.");
        });
    });

});