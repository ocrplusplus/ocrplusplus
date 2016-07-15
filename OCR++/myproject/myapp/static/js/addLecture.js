
$('#btnSubmit').click(function(e) {
    e.preventDefault() ;
	// console.log($("input[name=inputUserType]:checked").val());
	data = {
        'Notes' : $("#inputNotes").val(),
        'Date_Time' : $("#inputDate_Time").val(),
        'Topic' : $("#inputTopic").val(),
        'Link' : $("#inputLink").val(), 
        'Questions' : $("#inputQuestions").val(),
        'Answers' : $("#inputSolutions").val(),
    }

    console.log(data);
    $.ajax({
        url: '../addLecture/',
        dataType: 'json',
        contentType:'application/json',
        type: 'POST',
        data: JSON.stringify(data),
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