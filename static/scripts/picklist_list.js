$( function() {

    var rowId = 0;

    //Open picklist
    $('.view-edit-button').click( function() {
        rowId = this.parentElement.id;
        var request = $.get('/api/set_picklist_id', {picklist_id: rowId});
        request.done(function() {
            rowId = 0;
            getPicklist();
        });
    });

    //Delete picklist
    $('.delete-button').click( function() {
        rowId = this.parentElement.id;
        $('#confirmation-alert').fadeIn("fast");
        $('#background-cover').fadeIn("fast");
    });

    $('#confirmation-confirm').click( function() {
        var request = $.get('/api/delete_picklist', {picklist_id: rowId});
        request.done(function() {
            rowId = 0;
            location.reload();
        });
    });

    $('#confirmation-cancel').click( function() {
        rowId = 0
        $('#confirmation-alert').fadeOut("fast");
        $('#background-cover').fadeOut("fast");
    });
});