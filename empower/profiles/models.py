import hashlib

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.encoding import python_2_unicode_compatible
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
from allauth.account.signals import user_signed_up

# from django.contrib.auth.models import (
# 	BaseUserManager, AbstractBaseUser, PermissionsMixin)

class UserManager(BaseUserManager):
	def create_user(self, email, first_name, password=None):
		"""
		Creates and saves a User with the given
		name, email and password.
		"""
		if not first_name:
			msg = 'You must have a display name'
			raise ValueError(msg)

		if not email:
			msg = 'You must enter your email address'
			raise ValueError(msg)

		user = self.model(
			first_name=first_name,
			email=UserManager.normalize_email(email),
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, first_name, password):
		"""
		Creates and saves a superuser with the given
		name, email and password.
		"""
		user = self.create_user(email=email, first_name=first_name,  
			password=password)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
    """A site-specific user model.
    Important: You don't have to use a custom user model. I did it here because
    I didn't want a username to be part of the system and I wanted other data
    to be part of the user and not in a separate table. 
    You can avoid the username issue without writing a custom model but it
    becomes increasingly obtuse as time goes on. Write a custom user model, then
    add a custom admin form and model.
    Remember to change ``AUTH_USER_MODEL`` in ``settings.py``.
    """

    email = models.EmailField(_('email address'), blank=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=40, blank=False, unique=False)
    last_name = models.CharField(_('last name'), max_length=40, blank=True, null=True, unique=False)
    display_name = models.CharField(_('display name'), max_length=14, blank=True, null=True, unique=False)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name',)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'
        abstract = False

    def get_absolute_url(self):
        return "/profile/%s/" % (self.pk)  # TODO: email ok for this? better to have uuid?

    @property
    def name(self):
        if self.display_name:
            return self.display_name
        return self.first_name

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def guess_display_name(self):
        """Set a display name, if one isn't already set."""
        if self.display_name:
            return

        if self.first_name and self.last_name:
            dn = "%s %s" % (self.first_name, self.last_name[0]) # like "Andrew E"
        else:
            dn = self.first_name
        self.display_name = dn.strip()

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.email

    def natural_key(self):
        return (self.email,)


@python_2_unicode_compatible
class UserProfile(models.Model):
    """Profile data about a user.
    Certain data makes sense to be in the User model itself, but some
    is more "profile" data than "user" data. I think this is things like
    date-of-birth, favourite colour, etc. If you have domain-specific
    profile information you might create additional profile classes, like
    say UserGeologistProfile.
    """
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile')

    avatar_url = models.CharField(max_length=256, blank=True, null=True)

    dob = models.DateField(verbose_name="DOB", blank=True, null=True)

    social_profile = models.URLField(blank=True, null=True)

    def __str__(self):
        return force_text(self.user.email)

    class Meta():
        db_table = 'user_profile'


@receiver(user_signed_up)
def set_initial_user_names(request, user, sociallogin=None, **kwargs):
    """
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:
 
    sociallogin.account.provider  # e.g. 'twitter' 
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']
 
    See the socialaccount_socialaccount table for more in the 'extra_data' field.
    From http://birdhouse.org/blog/2013/12/03/django-allauth-retrieve-firstlast-names-from-fb-twitter-google/comment-page-1/
    """

    preferred_avatar_size_pixels=256

    picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
        hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
        preferred_avatar_size_pixels
    )
 
    if sociallogin:
        # Extract first / last names from social nets and store on User record
        if sociallogin.account.provider == 'twitter':
            name = sociallogin.account.extra_data['name']
            user.first_name = name.split()[0]
            user.last_name = name.split()[1]
            social_link = sociallogin.account.extra_data['link']
 
        if sociallogin.account.provider == 'facebook':
            user.first_name = sociallogin.account.extra_data['first_name']
            user.last_name = sociallogin.account.extra_data['last_name']
            #verified = sociallogin.account.extra_data['verified']
            picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
                sociallogin.account.uid, preferred_avatar_size_pixels)
            social_link = sociallogin.account.extra_data['link']
 
        if sociallogin.account.provider == 'google':
            user.first_name = sociallogin.account.extra_data['given_name']
            user.last_name = sociallogin.account.extra_data['family_name']
            #verified = sociallogin.account.extra_data['verified_email']
            picture_url = sociallogin.account.extra_data['picture']
            social_link = sociallogin.account.extra_data['link']
 
    profile = UserProfile(user=user, avatar_url=picture_url, social_profile=social_link)
    profile.save()

    user.guess_display_name()
    user.save()


