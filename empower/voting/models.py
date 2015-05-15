from datetime import datetime
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.auth import get_user_model
from django.db import models
from voting.managers import VoteManager

"""
Implementation of Upvote/No-vote functionality. 
Inspired by +1/0/-1 voting implementation in 
https://github.com/jezdez/django-voting	
"""

class Vote(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	vote = models.BooleanField(default=False)
	time_stamp = models.DateTimeField(editable=False, auto_now=True)

	objects = VoteManager()
	
	class Meta:
		unique_together = (('user', 'content_type', 'object_id'),)

	def __str__(self):
		return '%s upvoted - %s' %(self.user, self.content_object)