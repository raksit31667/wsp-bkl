function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });


  $(function() {
    $("#register-form").submit(function( event ) {
      event.preventDefault();
      var username = $("#register-username").val();
      var email = $("#register-email").val();
      var password = $('#register-password').val();
      var password2 = $('#register-password-confirm').val();
      var checkPolicy = $('#register-policy');
      var err = $("#register-error-message");

      registerable = true;
      msg = "";
      if (password!=password2){
        registerable = false;
        msg = "Passwords are not the same."
      }

      if(username==""||email==""||password==""||password2==""){
        registerable = false;
        msg = "Please complete all information requested on this form."
      }

      if (!checkPolicy.is(':checked')){
        registerable = false;
        msg = "Please accept our policy."
      }

      err.text(msg);

      if(registerable){
        $.ajax({
          url : '/movie/api/register/',
          type : 'POST',
          data : {username: username, email: email, password: password},
          success : function(response){
            if(response.registerable){
              $('#register-modal').modal('hide');
              $('#login-modal').modal('toggle');
              alert(response.msg);
            }else{
              err.text(response.msg);
            }
          }
        });
      }

    });

  });
