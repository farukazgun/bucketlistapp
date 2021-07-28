$(function(){
	$('#btnSignUp').click(function(){
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				res = JSON.parse(response);
				console.log(res.status);
				if (res.status === "false" ){
					$("#error-msg").html(res.error);
					$("#error-msg").show();
					return true;
				}
				$("#error-msg").hide();
				$("#success-msg").show();
				setTimeout(function() {
					window.location.href = "signin";
				}, 2000);
			},
			
			/*success: function(response){
				setTimeout(function () {
   					window.location.href = "blog.html"; //will redirect to your blog page (an ex: blog.html)
				}, 2000); //will call the function after 2 secs.
				/*alert('Thank For Sign Up');
				$("#succes-msg").show();
				setTimeout(function() {window.location.href = "showSignIn", 5000});
				setTimeout(function){window.location.href = "showSignIn", 5000;)}
			},*/
			error: function(error){
				console.log(error);
			}
		});
	});
});

