from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes import generic
from django.utils.text import slugify
from profiles.models import UserProfile
from voting.models import Vote

class TimeStampedModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Question(TimeStampedModel):
	title = models.TextField()
	slug = models.SlugField(unique=True)
	votes = generic.GenericRelation(Vote)

	def __unicode__(self):
		return self.title

	@models.permalink
	def get_absolute_url(self):
		return ('view_question', None, {'slug': self.slug})

	def save(self):
		super(Question, self).save()
		self.slug = slugify(self.title)
		super(Question, self).save()
	
	class Meta:
		ordering = ["-created"]


class Answer(TimeStampedModel):
	answer = models.TextField()
	question = models.ForeignKey(Question)
	answered_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	votes = generic.GenericRelation(Vote)
	anonymous = models.BooleanField(default=False, blank=False)

	def __unicode__(self):
		return "%s's answer to %s" %(self.answered_by.name, self.question.title)

	@models.permalink
	def get_absolute_url(self):
		return ('view_answer', None, {'id': self.id})

	def make_anonymous(self):
		if not self.anonymous:
			self.anonymous = True
			self.save()

	class Meta:
		ordering = ["-created"]
		unique_together = (('question', 'answered_by'),)

	# add a post_signal (question + answered_by -> unique)