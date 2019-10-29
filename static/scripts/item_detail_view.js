$(function() {

    //Show and hide add buttons
    $('.add-to-picklist-button').fadeTo(0, 0);

    $('.location-row').mouseenter(function() {
        $(this).children('.add-to-picklist-button').fadeTo(0, 100);
    });

    $('.location-row').mouseleave(function() {
        $(this).children('.add-to-picklist-button').fadeTo('fast', 0);
    });

    //Add to picklist
    $('.add-to-picklist-button').click(function() {        
        var locationItemId = this.parentElement.id;
        request = $.get('/api/add_item_to_picklist', {location_item_id: locationItemId});
        request.done(function() {
            getPicklist();
        });
        request.fail(function() {
            alert("An error occured. If there is no active picklist, please create a new one, or select one from the left sidebar.");
        });
    });

});