$( function() {

    //Open picklist
    $('.view-edit-button').click( function() {
        var rowId = this.parentElement.id;
        var request = $.get('/api/set_picklist_id', {picklist_id: rowId});
        request.done(function() {
            getPicklist()
        });
    });
});