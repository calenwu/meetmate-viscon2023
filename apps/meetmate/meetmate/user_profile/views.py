import logging
import json
import requests
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, View
from django.utils import timezone
from django.utils.translation import gettext as _

from datetime import datetime, timedelta

from allauth.account.views import (
	SignupView, 
	LoginView,
	PasswordChangeView,
	PasswordResetView,
	PasswordResetFromKeyView,
	PasswordSetView
)
from allauth.socialaccount.views import (
	ConnectionsView,
	SignupView as SocialSignupView
)

from core.utils import hx_redirect, hx_trigger

from user_profile.forms import (
	CustomSocialSignupForm,
	EditProfileForm,
	UserLoginForm,
	UserRegisterForm,
)
from user_profile.models import UserProfile


logger = logging.getLogger('django')


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('core:create'))


class CustomSocialSignupView(SocialSignupView):
	template_name = 'allauth/signup.html'
	form_class = CustomSocialSignupForm

	def form_invalid(self, form):
		return super().form_invalid(form)

	def form_valid(self, form):
		"""Adds the 'HX-Redirect' header for htmx to redirect to the dashboard"""
		super().form_valid(form)
		return HttpResponseRedirect(reverse('profile:login_verify', kwargs={'login': form.cleaned_data['username']}))


class CustomSignUpView(SignupView):
	"""allauth.account.views.SignupView"""
	template_name = 'user_profile/sign_up_form.html'
	form_class = UserRegisterForm

	def form_valid(self, form):
		"""Adds the 'HX-Redirect' header for htmx to redirect to the dashboard"""
		http_response = super().form_valid(form)
		# temp = form.cleaned_data['from_page']
		# if temp != '/':
		# 	return hx_redirect(http_response, temp)
		# return hx_redirect(http_response, reverse('profile:login_verify', kwargs={'login': form.cleaned_data['email']}))
		return hx_redirect(http_response, reverse('profile:edit_profile'))


class CustomSignInView(LoginView):
	"""allauth.account.views.LoginView"""
	template_name = 'user_profile/sign_in_form.html'
	form_class = UserLoginForm

	def form_valid(self, form):
		"""Adds the 'HX-Redirect' header for htmx to redirect to the dashboard"""
		http_response = super().form_valid(form)
		login = form.cleaned_data['login']
		logger.info(login)
		user = UserProfile.objects.get(email__iexact=login)
		return hx_redirect(http_response, reverse('profile:edit_profile'))


class CustomPasswordResetView(PasswordResetView):
	"""allauth.account.views.PasswordReset.view"""
	template_name = 'user_profile/password_reset_form.html'
	success_url = reverse_lazy('profile:password_reset_form')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['success'] = False
		return context

	def form_valid(self, form):
		"""Adds the 'HX-Redirect' header for htmx to redirect to the dashboard"""
		super().form_valid(form)
		context = super().get_context_data()
		context['success'] = True
		http_response = self.render_to_response(context)
		return http_response


class CustomPasswordSetView(LoginRequiredMixin, PasswordSetView):
	def form_valid(self, form):
		return super().form_valid(form)


class EditProfileView(LoginRequiredMixin, UpdateView):
	form_class = EditProfileForm
	template_name = 'user_profile/edit.html'
	success_url = reverse_lazy('profile:edit_profile')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'request': self.request})
		kwargs.update({'initial_email': self.request.user.email})
		return kwargs

	def get_object(self, queryset=None):
		return self.request.user

	def form_valid(self, form):
		"""Adds the 'HX-Redirect' header for htmx to redirect to the dashboard"""
		messages.success(
			self.request,
			json.dumps({
				'data': {
					'title': str(_('Profile updated')),
					'innerHTML': str(_('Your profile has been updated.')),
					'type': 'success'
				}
			})
		)
		return super().form_valid(form)


class UserProfileDetailsView(DetailView):
	model = UserProfile
	slug_url_kwarg = 'username'
	slug_field = 'username'
	template_name = 'user_profile/details.html'

	def get_object(self, queryset=None):
		return get_object_or_404(UserProfile.objects.filter(disabled=False), username=self.kwargs['username'])

	def get_context_data(self, **kwargs):
		context = super(UserProfileDetailsView, self).get_context_data(**kwargs)
		context['paypal_client_id'] = settings.PAYPAL_CLIENT_ID
		context['paypal_merchant_id'] = settings.PAYPAL_MERCHANT_ID
		return context
