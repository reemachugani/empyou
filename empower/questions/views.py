from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.forms import ModelForm, Textarea
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Question, Answer
from notifications import notify
from notifications.models import Notification
from voting.models import Vote
import json

class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ['answer', 'anonymous']
		widgets = {
			'answer' : Textarea(attrs={'rows': 6, 'style': 'width: 100%;'}),
		}

def home(request):
	"""
	displays the last added question and the answers to it
	"""
	# add an if statement to redirect the url to signup page or home based on user authentication

	ques = Question.objects.all()[0]
	return render_question_page(request, ques)

def all_questions_page(request):
	"""
	displays all the questions
	"""
	return render_to_response('questions/all_questions_page.html', {'questions': Question.objects.all()}, context_instance=RequestContext(request))

def view_question_page(request, slug):
	"""
	displays question page based on slug value
	"""
	ques = Question.objects.get(slug=slug)
	return render_question_page(request, ques)

def render_question_page(request, question):
	"""
	renders the question page based on if user has answered already
	"""
	if request.method == "POST":
		form = AnswerForm(request.POST)
		if form.is_valid():
			answer = form.save(commit=False)
			answer.question = question
			answer.answered_by = request.user
			answer.save()		
	answers = question.answer_set.all()
	can_answer = can_user_answer(request, question)
	form = AnswerForm()
	votes_from_user = Vote.objects.get_for_user_in_bulk(answers, request.user)
	return render_to_response('questions/question_page.html', {'question': question, 'answers': answers, 'can_answer': can_answer, 'form': form, 'votes_from_user': votes_from_user}, context_instance=RequestContext(request))

def can_user_answer(request, ques):
	"""
	checks if user has already answered the given question
	"""
	if request.user.is_authenticated():
		ans = Answer.objects.filter(question=ques, answered_by__email=request.user.get_username)
		if not ans:
			return True		
	return False

@login_required
def vote_answer(request, ans_id):
	"""
	handles the upvoting event, updates the Vote model, and sends notification to User
	"""
	if request.method == 'POST':
		vote = (request.POST.get('vote') == "true")
		answer = Answer.objects.get(pk=ans_id)
		Vote.objects.record_vote(answer, request.user, vote)
		if vote:
			notify.send(request.user, recipient=answer.answered_by, verb=u'upvoted', action_object=answer, target=answer)
		else:
			notification_old = Notification.objects.filter(actor_object_id=request.user.id, verb=u'upvoted', action_object_object_id=ans_id)
			if notification_old:
				notification_old[0].delete()
		response_data = {}
		response_data['updated_vote'] = Vote.objects.get_votes(answer)
		response_data['pk'] = answer.pk
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)
	return HttpResponse(
			json.dumps({"nothing to see": "this isn't happening"}),
			content_type="application/json"
		)

def view_answer_page(request, id):
	"""
	displays the answer page based on the id
	"""
	answer = Answer.objects.get(id=id)
	vote_from_user = (Vote.objects.get_for_user(answer, request.user) != None)
	return render_to_response('questions/answer_page.html', {'answer': answer, 'vote_from_user': vote_from_user}, context_instance=RequestContext(request))
