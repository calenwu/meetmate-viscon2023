import json
import pytz

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.templatetags.static import static

from allauth.account.models import EmailAddress
from .utils import file_size


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_staff') is False:
			raise ValueError(
				'Superuser must have is_staff=True.'
			)
		if extra_fields.get('is_superuser') is False:
			raise ValueError(
				'Superuser must have is_superuser=True.'
			)
		return self._create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
	username = None
	email = models.EmailField('email address', unique=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = UserManager()
	profile_picture = models.ImageField(
		upload_to='user_profiles/profile_pictures',
		validators=[file_size],
		blank=True,
		null=True)
	about_me = models.TextField(max_length=4095, blank=True, null=True)
	disabled = models.BooleanField(default=False)

	def __str__(self):
		return self.email
		# return self.first_name + ' ' + self.last_name

	@property
	def display_banner_url(self) -> str:
		return self.banner.url if self.banner else static('img/default_banner.webp')

	@property
	def display_profile_picture_url(self) -> str:
		return self.profile_picture.url if self.profile_picture else static('img/default_profile_picture.svg')

	@property
	def display_name(self) -> str:
		return '{} {}'.format(self.first_name, self.last_name)

	@property
	def display_about_me(self) -> str:
		return self.about_me if self.about_me else ''

	def get_absolute_url(self):
		return reverse('profile_detail:detail', kwargs={'username': str(self.username)})

	def add_email_address(self, request, new_email):
		return EmailAddress.objects.add_email(request, self, new_email, confirm=True)
