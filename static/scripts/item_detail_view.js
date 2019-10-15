$(function() {

    //Show and hide stock in/out form
    $('#stock-in-out-button').click( function() {     
        $('#stock-in-out-frame').css('display', 'block');
        $('#background-cover').css('display', 'block');
    });
    
    $('#background-cover').click( function() {
        $('#background-cover').css('display', 'none');
        $('#stock-in-out-frame').css('display', 'none');
    });

    //Add location
    $('#add-location-button').click( function() {
        const addLocationTextbox = document.getElementById('add-location-textbox');
        addLocationTextbox.setCustomValidity('Enter a valid location name. (ex. "301A01A")');
        var locationLabels = document.getElementsByClassName('location-label');        
        var locationNames = [];
        for (var i = 0; i < locationLabels.length; i++) {
            locationNames.push(locationLabels[i].innerHTML.toUpperCase());
        }
        if (!addLocationTextbox.validity.patternMismatch) {
            const locationName = addLocationTextbox.value.toUpperCase().trim();
            if (locationNames.includes(locationName)) {
                addLocationTextbox.setCustomValidity('Location already exists.');
                addLocationTextbox.reportValidity();
                return
            }
            $.get('/api/new_location', {location_name: locationName}).done(function (data) {
                const location = data;
                const locationLabel = document.createElement('label');
                const quantityInput = document.createElement('input');
                locationLabel.htmlFor = location['location_id'];
                locationLabel.innerHTML = location['location_name'].toUpperCase();
                quantityInput.type = "number";
                quantityInput.defaultValue = 0;
                const locationFieldSet = document.getElementById('locations-fieldset');
                locationFieldSet.appendChild(locationLabel);
                locationFieldSet.appendChild(quantityInput);
                locationFieldSet.appendChild(document.createElement('br'));
                addLocationTextbox.value = "";
            })         
            
        } else {
            addLocationTextbox.reportValidity();
        }
    });
});