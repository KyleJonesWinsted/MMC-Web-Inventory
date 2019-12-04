$(window).bind("pageshow", function(event) {
    if (event.originalEvent.persisted) {
        this.getPicklist()
    }
});

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
getPicklist()

function getPicklist() {
    $('#picklist-frame').load('/api/get_picklist');
}

//Logout

function logout() {
    request = $.get('/logout');
    request.done(function() {
        window.location.assign("/login");
    });
    request.fail(function() {
        alert('Unable to logout. Please reload and try again.')
    });
}
$(function() {
    idleTimer();

    $('#logout-button').click(function() {
        $(this).attr('disabled', true)
        logout();
    });
});

function idleTimer() {
    var t;
    //window.onload = resetTimer;
    window.onmousemove = resetTimer; // catches mouse movements
    window.onmousedown = resetTimer; // catches mouse movements
    window.onclick = resetTimer;     // catches mouse clicks
    window.onscroll = resetTimer;    // catches scrolling
    window.onkeypress = resetTimer;  //catches keyboard actions
    resetTimer()

    function resetTimer() {
        clearTimeout(t);
        t = setTimeout(logout, 300000);  // time is in milliseconds (1000 is 1 second)
        //t= setTimeout(reload, 300000);  // time is in milliseconds (1000 is 1 second)
    }
}

//Show and hide sidebar and picklist on mobile

$(function() {

    $('#show-sidebar-button').click(function() {
        $('#sidebar').show()
        $('#hide-sidebar-button').show()
        $('#white-cover').show()
    });

    $('#show-picklist-button').click(function() {
        $('#picklist-frame').show()
        $('#hide-picklist-button').show()
        $('#white-cover').show()
    });

    $('#hide-picklist-button').click(function() {
        $('#picklist-frame').hide()
        $('#hide-picklist-button').hide()
        $('#white-cover').hide()
    });

    $('#hide-sidebar-button').click(function() {
        $('#sidebar').hide()
        $('#hide-sidebar-button').hide()
        $('#white-cover').hide()
    });
});
