from django.db import models
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

class VoteManager(models.Manager):
	"""
	Implementation of Upvote/No-vote functionality. 
	Inspired by +1/0/-1 voting implementation in 
	https://github.com/jezdez/django-voting	
	"""
	def get_votes(self, obj):
		"""
		Gets total votes for 'obj'
		"""
		ctype = ContentType.objects.get_for_model(obj)
		votes = self.filter(object_id=obj._get_pk_val(), content_type=ctype).count()
		return votes

	def get_votes_in_bulk(self, objects):
		"""
		Gets total votes for all objects.
		"""
		object_ids = [o._get_pk_val() for o in objects]
		if not object_ids:
			return {}
		ctype =  ContentType.objects.get_for_model(objects[0])
		queryset = self.filter(object_id__in=object_ids, content_type=ctype,).values('object_id',).annotate(votes=Count('vote'))
		vote_dict = {}
		for obj in objects:
			vote_dict[obj] = 0
		for row in queryset:
			vote_dict[row['object_id']] = int(row['votes'])
		return vote_dict

	def record_vote(self, obj, user, vote):
		"""
		Records a user's vote on a given object. Only allows user to vote once,
		though the vote can be changed.
		Vote=False indicates that an existing vote should be removed.
		"""
		ctype = ContentType.objects.get_for_model(obj)
		try:
			v = self.get(user=user, content_type=ctype, object_id=obj._get_pk_val())
			if vote == False:
				v.delete()
		except models.ObjectDoesNotExist:
			if vote == False:
				return
			self.create(user=user, content_type=ctype, object_id=obj._get_pk_val(), vote=vote)    		

	def get_top(self, model, limit=10, reversed=False):
		"""
		Get the top N voted objects for a given model.
		Yields (object, score) tuples.
		"""
		ctype = ContentType.objects.get_for_model(model)
		results = self.filter(content_type=ctype).values('object_id').annotate(votes=Count('vote'))
		if reversed:
			results = results.order_by('votes')
		else:
			results = results.order_by('-votes')

		# Use in_bulk() to avoid O(limit) db hits.
		objects = model.objects.in_bulk([item['object_id'] for item in results[:limit]])

		top_dict = {}
		# Yield each object, score pair. Because of the lazy nature of generic
		# relations, missing objects are silently ignored.
		for item in results[:limit]:
			id, votes = item['object_id'], item['votes']
			if not votes:
				top_dict[objects[id]]=0
			if id in objects:
				top_dict[objects[id]]=int(votes)
		return top_dict

	def get_bottom(self, model, limit=10):
		"""
		Get the bottom (most unpopular) N voted objects for a given model.
		Yields (object, score) tuples.
		"""            
		return self.get_top(model, limit, True)

	def get_for_user(self, obj, user):
		"""
		Get the vote made on the given object by the given user, or
		``None`` if no matching vote exists.
		"""
		if not user.is_authenticated():
			return None
		ctype = ContentType.objects.get_for_model(obj)
		try:
			vote = self.get(content_type=ctype, object_id=obj._get_pk_val(),
							user=user)
		except models.ObjectDoesNotExist:
			vote = None
		return vote

	def get_for_user_in_bulk(self, objects, user):
		"""
		Get a dictionary mapping object ids to votes made by the given
		user on the corresponding objects.
		"""
		vote_dict = {}
		if len(objects) > 0:
			ctype = ContentType.objects.get_for_model(objects[0])
			votes = list(self.filter(content_type__pk=ctype.id,
									object_id__in=[obj._get_pk_val() \
									for obj in objects],
									user__pk=user.id))
			vote_dict = dict([(vote.object_id, vote) for vote in votes])
		return vote_dict
