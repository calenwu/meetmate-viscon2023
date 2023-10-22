from django.urls import path
from .views import UserProfileDetailsView

urlpatterns = [
	path('<str:username>', UserProfileDetailsView.as_view(), name='detail')
]
