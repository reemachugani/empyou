from django.db import models
from profiles.models import UserProfile
from django.contrib.auth import get_user_model

class TimeStampedModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Question(TimeStampedModel):
	question = models.TextField()

	def __unicode__(self):
		return self.question

	class Meta:
		ordering = ["-created"]


class Answer(TimeStampedModel):
	answer = models.TextField()
	question = models.ForeignKey(Question)
	answered_by = models.ForeignKey(get_user_model())
	upvotes = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return "%s's answer to %s" %(self.answered_by.name, self.question.question)

	class Meta:
		ordering = ["-created"]

	# add a post_signal (question + answered_by -> unique)