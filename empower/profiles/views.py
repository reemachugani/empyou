from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import UserProfile
from questions.models import Question, Answer
from voting.models import Vote

def profile_page(request, id):
	"""
	displays user details and questions answered
	"""
	profile_user = get_object_or_404(UserProfile, pk=id)
	answers = Answer.objects.filter(answered_by = profile_user.user)
	votes_from_user = Vote.objects.get_for_user_in_bulk(answers, request.user)
	return render_to_response('profiles/profile_page.html', {'profile_user': profile_user, 'answers': answers, 'votes_from_user': votes_from_user}, context_instance=RequestContext(request))