$(function(){
	$('button').click(function(){
		var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();
		$.ajax({
			url: '/signUpUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});

$(function(){
	$('button').click(function(){
		var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();
		$('p').text("Congratulations on registering for CSE6242 " + user + " Redirecting you to the course homepage...");
		$('form')[0].reset();
	});
});

$(function() {
    $('button').click(function () {
        setTimeout("window.location.href='http://poloclub.gatech.edu/cse6242/2018spring/';",3000);
    });
});

