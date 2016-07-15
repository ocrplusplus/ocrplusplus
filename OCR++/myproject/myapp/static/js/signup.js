// var photoDataUrl = ""
// function previewFile() {
//   var preview = document.querySelector('#profile-pic');
//   var file    = document.querySelector('#image').files[0];
//   var reader  = new FileReader();
//
//   reader.onloadend = function () {
//     preview.src = reader.result;
//   }
//
//   if (file) {
//     console.log(reader.readAsDataURL(file))
//     photoDataUrl = reader.readAsDataURL(file);
//   } else {
//     preview.src = "";
//   }
// }



$('#btnSignUp').click(function(e) {
    e.preventDefault() ;
	// console.log($("input[name=inputUserType]:checked").val());
	var flag = 0;
	if($("input[name=inputUserType]:checked").val() === "student") flag = 1;
	else if($("input[name=inputUserType]:checked").val() === "faculty") flag = 2;
    user = {
        'name' : $("#inputName").val(),
        'email' : $("#inputEmail").val(),
        'password' : $("#inputPassword").val(),
		'dob' : $("#inputDOB").val(),
        'flag' : flag
    }

    console.log(user);

    $("#status").html('waiting...');

    $.ajax({
        url: '../signUp/',
        dataType: 'json',
        contentType:'application/json',
        type: 'POST',
        data: JSON.stringify(user),
        success: function(response) {
            console.log("user added");
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

});
