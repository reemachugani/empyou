from questions.models import Question
from voting.models import Vote
from notifications.models import Notification

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

def unread_notifications(request):
	all_notifications = Notification.objects.filter(recipient_id=request.user.id)
	return {'all_notifications': all_notifications, 'unread_notifications_count': all_notifications.unread().count()}