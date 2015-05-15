from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import notifications

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'questions.views.home', name='home'),
    url(r'^question/', include('questions.urls')),
    url(r'^profile/', include('profiles.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^inbox/notifications/', include(notifications.urls)),
)

if settings.DEBUG:
	import debug_toolbar
	urlpatterns += patterns('',
		url(r'^__debug__/', include(debug_toolbar.urls)),
	)