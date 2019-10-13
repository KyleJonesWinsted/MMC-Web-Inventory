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
        if (!addLocationTextbox.validity.patternMismatch) {
            locationName = addLocationTextbox.value.toUpperCase();           
            locationLabel = document.createElement('label');
            quantityInput = document.createElement('input');
            locationLabel.htmlFor = locationName;
            locationLabel.innerHTML = locationName;
            quantityInput.type = "number";
            quantityInput.defaultValue = 0;
            locationFieldSet = document.getElementById('locations-fieldset');
            locationFieldSet.appendChild(locationLabel);
            locationFieldSet.appendChild(quantityInput);
            locationFieldSet.appendChild(document.createElement('br'));

            addLocationTextbox.value = "";
        } else {
            addLocationTextbox.reportValidity();
        }
    });
});