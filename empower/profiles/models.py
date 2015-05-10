from django.db import models

from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser, PermissionsMixin)

class UserManager(BaseUserManager):
	def create_user(self, name, email, password=None):
		"""
		Creates and saves a User with the given
		name, email and password.
		"""
		if not name:
			msg = 'You must have a display name'
			raise ValueError(msg)

		if not email:
			msg = 'You must enter your email address'
			raise ValueError(msg)

		user = self.model(
			name=name,
			email=UserManager.normalize_email(email),
		)
		user.set_password(password)
		user.is_staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, name, email, password):
		"""
		Creates and saves a superuser with the given
		name, email and password.
		"""
		user = self.create_user(name=name, email=email, 
			password=password)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
	"""
	Inherits from both the AbstractBaseUser and
	PermissionMixin
	"""
	name = models.CharField(max_length=255)
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
		db_index=True,)

	USERNAME_FIELD = 'email'	# returned when get_username() is called
	REQUIRED_FIELDS = ['name', ]

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	# is_superuser = models.BooleanField(default=False)

	objects = UserManager()

	def get_short_name(self):
		return self.name

	def get_full_name(self):
		return "%s has registered with %s" %(self.name, self.email)

	def __unicode__(self):
		return self.email





