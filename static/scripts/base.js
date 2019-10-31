// Search box functionality
const searchBox = document.getElementById('search-box');
const searchButton = document.getElementById('search-button');
searchButton.addEventListener("click", search);
searchBox.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        search()
    }
});

function search() {
    var searchValue = searchBox.value;
    const searchString = searchValue.trim()
    if (searchString.length < 3) {
        searchBox.style.border = '3px solid red';
        searchBox.setCustomValidity('Please enter a longer search term.');
        searchBox.reportValidity();
        return
    }
    const baseURL = '/search?input='
    // Will probably change later to escape on the server side
    window.location.assign(baseURL + encodeURI(searchString)) 
}

//Picklist functionality
const $picklistFrame = $('#picklist-frame');

getPicklist()

function getPicklist() {
    $picklistFrame.load('/api/get_picklist');
}

//Logout
$(function() {
    $('#logout-button').click(function() {
        request = $.get('/logout');
        request.done(function() {
            window.location.assign("/login");
        });
        request.fail(function() {
            alert('Unable to logout. Please reload and try again.')
        });
    });
})