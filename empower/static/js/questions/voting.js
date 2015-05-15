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
	$('.upvote').on('click',function(){
		$.ajax({
			data: { vote: (($(this).text() == "Like")? "true" : "false") },
			type: 'POST',
			url: $(this).data('update-url'),

			success : function(json) {
				console.log(json); // log the returned json to the console
				if(json.updated_vote == 1)
					$("#answer-vote-count-" + json.pk).text(json.updated_vote + " vote");
				else
					$("#answer-vote-count-" + json.pk).text(json.updated_vote + " votes");
				console.log("success"); // another sanity check
				if($('#upvote-' + json.pk).text() == "Dislike")
					$('#upvote-' + json.pk).text("Like");
				else
					$('#upvote-' + json.pk).text("Dislike");
			},
		});
	}); 
});