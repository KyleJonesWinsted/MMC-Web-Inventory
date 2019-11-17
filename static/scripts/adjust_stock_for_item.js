$( function() {

    //Blank reason dropdown
    $("#reason").prop("selectedIndex", -1);

    //Add location
    $('#add-location-button').click( function() {
        const addLocationTextbox = document.getElementById('add-location-textbox');
        addLocationTextbox.setCustomValidity('Enter a valid location name. (ex. "301A01A")');
        var locationLabels = document.getElementsByClassName('location-label');        
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
            $.get('/api/new_location', {location_name: locationName}).done(function (data) {
                const location = data;
                const locationLabel = document.createElement('label');
                const quantityInput = document.createElement('input');
                locationLabel.htmlFor = location['location_id'];
                locationLabel.className = 'location-label';
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