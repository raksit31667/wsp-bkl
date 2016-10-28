$(function() {
  $("#login-form").submit(function( event ) {
    event.preventDefault();
    var username = $("#login-username").val();
    var password = $('#login-password').val();

    $.ajax({
      url : '/movie/api/login/',
      type : 'GET',
      data : {username: username, password: password},
      success : function(response){
        if(response.data == 1){
          window.location.href = "/";
        }
        else{
          $("#error-message").text(response.msg);
        }
      }
    });

    // Post to Server
    // $.ajax({
    // 	type: "POST",
    // 	url: "http://localhost:4000/login",
    //
    // 	data: JSON.stringify({
    // 		username: username,
    // 		password: password
    // 	}),
    // 	contentType: "application/json; charset=utf-8",
    //     dataType: "json",
    //     success: function(data){
    //     	if(data.msg === 'done') {
    //     		window.location.href = "/";
    //     	}
    //
    //     	if(data.error) {
    //     		$('.error-message').text(data.error);
    //     	}
    //     },
    //   error: function(data) {
    //   	console.log(data);
    //   }
    // });
  });

});
