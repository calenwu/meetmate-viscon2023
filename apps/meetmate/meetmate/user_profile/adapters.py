import re
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

# https://owasp.org/www-community/password-special-characters
special_characters = " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"


class CustomAccountAdapter(DefaultAccountAdapter):
	max_email_length = 254
	min_password_length = 8
	max_password_length = 128

	def clean_email(self, email):
		if len(email) > self.max_email_length:
			raise ValidationError(
				_('Your email cannot be longer than {} characters.'.format(self.max_email_length)),
				code='email_too_long',
			)
		return super().clean_email(email)

	def clean_password(self, password, user=None):
		if len(password) < self.min_password_length:
			raise ValidationError(
				_('Your password cannot be shorter than {} characters.'.format(self.min_password_length)),
				code='password_too_short',
			)
		if len(password) > self.max_password_length:
			raise ValidationError(
				_('Your password cannot be longer than {} characters.'.format(self.max_password_length)),
				code='password_too_long',
			)
		return super().clean_password(password)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
	# def get_login_redirect_url(self, request):
	# 	path = "/accounts/{username}/"
	# 	return path.format(username=request.user.username)

	def save_user(self, request, sociallogin, form=None):
		super(SocialAccountAdapter, self).save_user(request, sociallogin, form=form)
		return redirect('profile:edit_profile')
