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

$(document).ready(function(){
	$('#upvote').on('click',function(){
		alert($(this).text()=="Like");
		$.ajax({
			data: { vote: (($(this).text() == "Like")? "true" : "false") },
			type: 'POST',
			url: $(this).data('update-url'),

			success : function(json) {
				console.log(json); // log the returned json to the console
				$("#ans-vote-count").text(json.updated_vote);
				console.log("success"); // another sanity check
				alert(json.updated_vote);
				$.each({{votes_from_user}}, function(key, value){
					if(parseInt($(this).data('answer-pk') == key)
						$(this).text("Dislike");
					else
						$(this).text("Like");
				});
			},

		});
		alert("upvoted");
	}); 
});