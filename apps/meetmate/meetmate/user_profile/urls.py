from django.urls import path, re_path
from .views import (
	CustomSignUpView,
	CustomSignInView,
	CustomPasswordResetView,
	CustomSocialSignupView,
	EditProfileView,
	logout_view,
	CustomPasswordSetView,
)

urlpatterns = [
	path('logout/', logout_view, name='logout'),
	path('sign-up-form/', CustomSignUpView.as_view(), name='sign_up_form'),
	path('sign-in-form/', CustomSignInView.as_view(), name='sign_in_form'),
	path('password-reset-form/', CustomPasswordResetView.as_view(), name='password_reset_form'),
	path('password-set-form/', CustomPasswordSetView.as_view(), name='password_set_form'),
	path('edit/', EditProfileView.as_view(), name='edit_profile'),
	path('social/signup/', CustomSocialSignupView.as_view(), name='custom_social_signup'),

	# path('login-form/verify/', VerifySignInView.as_view(), name='login_verify_form'),
	# path('login-form/verify/<str:login>/', VerifySignInView.as_view(), name='login_verify_form'),
]
