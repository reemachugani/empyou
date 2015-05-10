from django.conf.urls import patterns, url
from questions import views

urlpatterns = patterns('questions.views',
	url(r'^all/$', 'all_questions_page', name='all_questions'),
	#example: /question/vote-answer/233/
	url(r'^vote-answer/(?P<ans_id>\d+)/$', 'vote_answer', name='vote_answer'), 
	#example: /question/some-question-title/
    url(r'^(?P<slug>[^\.]+)/$', 'view_question_page', name='view_question'),
)