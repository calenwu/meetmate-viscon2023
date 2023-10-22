import json
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext as _
from allauth.account.admin import EmailAddress
from allauth.account.forms import (
	SignupForm,
	LoginForm
)
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from user_profile.models import UserProfile
from core.utils import convert_to_smallest_unit, non_float_currs


class CustomSocialSignupForm(SocialSignupForm):
	first_name = forms.CharField(label=_('First name'), max_length=30)
	last_name = forms.CharField(label=_('Last name'), max_length=30)

	# class Meta:
	# 	model = UserProfile
	# 	fields = ['username', 'email', 'first_name', 'last_name']

	# def __init__(self, sociallogin=None, *args, **kwargs):
	# 	kwargs['initial'] = get_adapter().get_signup_form_initial_data(sociallogin)
	# 	super().__init__(*args, **kwargs)

	def signup(self, request, user):
		user = super().signup(self, request, user)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()


class UserLoginForm(LoginForm):
	from_page = forms.CharField(required=False)

	class Meta:
		model = UserProfile
		fields = ['login', 'password']


class UserRegisterForm(SignupForm):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	from_page = forms.CharField(required=False)

	class Meta:
		model = UserProfile
		fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

	def clean(self):
		cleaned_data = self.cleaned_data
		if 'email' not in cleaned_data.keys():
			raise forms.ValidationError('Please check your input.')
		cleaned_data['username'] = cleaned_data['email']
		return cleaned_data

	def clean_username(self):
		return self.cleaned_data['email']

	def clean_email(self):
		users = UserProfile.objects.filter(email=self.cleaned_data['email'])
		if users.exists():
			raise forms.ValidationError('User with this email already exists.')
		return self.cleaned_data['email']


class UserLoginForm(LoginForm):
	from_page = forms.CharField(required=False)

	class Meta:
		model = UserProfile
		fields = ['login', 'password']


# check with adapters.py
class EditProfileForm(forms.ModelForm):
	first_name = forms.CharField(label=_('First name'), max_length=30)
	last_name = forms.CharField(label=_('Last name'), max_length=30)

	class Meta:
		model = UserProfile
		fields = [
			'first_name',
			'last_name',
			'email',
			'profile_picture',
			'about_me',
			# 'instagram',
			# 'twitter',
			# 'tiktok',
			# 'github','
		]

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.initial_email = kwargs.pop('initial_email', None)
		super(EditProfileForm, self).__init__(*args, **kwargs)
