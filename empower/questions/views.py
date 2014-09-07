from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Question, Answer
import user

def home(request):
	"""
	displays the last added question and the answers to it
	"""
	# add an if statement to redirect the url to signup page or home based on user authentication
	ques = Question.objects.filter()[0]
	answers = Answer.objects.filter(question__question = ques)
	can_answer = can_user_answer(request, question=ques)
	return render_to_response('questions/question_page.html', {'question': ques, 'answers': answers, 'can_answer': True}, context_instance=RequestContext(request))

def can_user_answer(request, question):
	"""
	checks if user has already answered the given question
	"""
	if request.user.is_authenticated():
		ques = Question.objects.filter(answer__question = question, answer__answered_by = request.user)
		if ques is None:
			return True		
	return False
