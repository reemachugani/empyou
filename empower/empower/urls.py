from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import notifications

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'questions.views.home', name='home'),
    url(r'^question/', include('questions.urls')),
    url(r'^profile/', include('profiles.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^inbox/notifications/', include(notifications.urls)),
)

if settings.DEBUG:
	import debug_toolbar
	urlpatterns += patterns('',
		url(r'^__debug__/', include(debug_toolbar.urls)),
	)