from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.contrib.contenttypes import generic
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
	answered_by = models.ForeignKey(get_user_model())
	votes = generic.GenericRelation(Vote)

	def __unicode__(self):
		return "%s's answer to %s" %(self.answered_by.name, self.question.title)

	class Meta:
		ordering = ["-created"]
		unique_together = (('question', 'answered_by'),)

	# add a post_signal (question + answered_by -> unique)