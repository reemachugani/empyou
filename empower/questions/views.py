from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Question, Answer
from voting.models import Vote
from django.forms import ModelForm, Textarea

class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ['answer']
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
	answers = Answer.objects.filter(question = question)
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