from django.urls import path
from django.views.generic import TemplateView

from .views import HomeView, EventCreateView, EventListView, EventDetailView, EventMemberDeleteView,\
		ScheduleEventDetailView

urlpatterns = [
	# path('', HomeView.as_view(), name='home'),
	path('favicon.ico', HomeView.as_view(), name='home'),
	path('events', EventListView.as_view(), name='events'),
	path('delete/<str:id>', EventMemberDeleteView.as_view(), name='event_member_delete'),
	path('<str:id>/google-calendar', EventMemberDeleteView.as_view(), name='google_calendar'),
	path('<str:id>/schedule', ScheduleEventDetailView.as_view(), name='schedule_detail'),
	path('<str:id>', EventDetailView.as_view(), name='detail'),
	path('', EventCreateView.as_view(), name='create'),
]
