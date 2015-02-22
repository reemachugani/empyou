from django.conf.urls import patterns, url
from questions import views

urlpatterns = patterns('questions.views',
	url(r'^all/$', 'all_questions_page', name='all_questions'),
	#example: /question/some-question-title/
    url(r'^(?P<slug>[^\.]+)/$', 'view_question_page', name='view_question'),    
)