from django.conf.urls import patterns, url
from profiles import views

urlpatterns = patterns('profiles.views',
	#example: /profile/233/
    url(r'^(?P<id>\d+)/$', 'profile_page', name='profile_page'),
)