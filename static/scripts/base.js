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
    var searchString = searchBox.value;
    if (searchString == "") { return; }
    const baseURL = '/search/'
    // Will probably change later to escape on the server side
    location.replace(baseURL + encodeURI(searchString)) 
}