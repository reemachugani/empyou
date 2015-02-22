from questions.models import Question
from voting.models import Vote

def recent_questions(request):
	questions = Question.objects.all()
	if questions.count > 5:
		questions = questions[0:5] 
	return {'recent_questions': questions}

def popular_questions(request):
	questions_count = Question.objects.count()
	question_votes_dict = {}
	if questions_count > 5:
		question_votes_dict = Vote.objects.get_top(Question, 5)
	else:
		questions = Question.objects.all()
		all_votes = Vote.objects.get_votes_in_bulk(questions)
		for ques in questions:
			question_votes_dict[ques] = all_votes[ques]
	return {'popular_questions': question_votes_dict}

