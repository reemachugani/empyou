from django.conf.urls import patterns, url
from questions import views

urlpatterns = patterns('questions.views',
	#example: /question/some-question-title/
    url(r'^(?P<slug>[^\.]+)/$', 'view_question_page', name='view_question'),
)