from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import UserProfile
from questions.models import Question, Answer
from voting.models import Vote

def profile_page(request):
	"""
	displays user details and questions answered
	"""
	user = request.user
	answers = Answer.objects.filter(answered_by = request.user)
	return render_to_response('profiles/profile_page.html', {'user': user, 'answers': answers}, context_instance=RequestContext(request))