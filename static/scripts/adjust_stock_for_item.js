$( function() {

    //Blank reason dropdown
    $("#reason").prop("selectedIndex", -1);

    //Add location
    $('#add-location-button').click( function() {
        const addLocationTextbox = document.getElementById('add-location-textbox');
        addLocationTextbox.setCustomValidity('Enter a valid location name. (ex. "301A01A")');
        var locationLabels = document.getElementsByClassName('location-label');
        var itemSKU = document.getElementById('item-sku').value;       
        var locationNames = [];
        for (var i = 0; i < locationLabels.length; i++) {
            locationNames.push(locationLabels[i].innerHTML.toLowerCase());
        }
        if (!addLocationTextbox.validity.patternMismatch) {
            const locationName = addLocationTextbox.value.toLowerCase().trim();
            if (locationNames.includes(locationName)) {
                addLocationTextbox.setCustomValidity('Location already exists.');
                addLocationTextbox.reportValidity();
                return
            }
            var request = $.get('/api/new_location', {location_name: locationName, item_sku: itemSKU});
            request.done(function (data) {
                window.location.reload();
            });
            request.fail(function() {
                alert("Unable to add new location. Please reload and try again.");
            });            
        } else {
            addLocationTextbox.reportValidity();
        }
    });
});