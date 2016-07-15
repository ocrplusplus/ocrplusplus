
$('#btnReset').click(function(e) {
    e.preventDefault() ;
	// console.log($("input[name=inputUserType]:checked").val());
	user = {
        'name' : $("#inputName").val(),
        'email' : $("#inputEmail").val(),
        'password' : $("#inputPassword").val(),
    }

    console.log(user);
    $.ajax({
        url: '../forgotPassword/',
        dataType: 'json',
        contentType:'application/json',
        type: 'POST',
        data: JSON.stringify(user),
        success: function(response) {
            window.location = (response)
            console.log(response);
            console.log("Password has been Reset");
            console.log(response.url);
            // data = JSON.parse(response) ;
            window.location = response.url ;
        },
        error: function(error) {
            console.log(error);
        },
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }

    });
    setTimeout(function() {
        // $this.addClass('ok');
        // $state.html('Welcome back!');
        console.log("error");
    }, 10000);
});