import collections
import json

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, DeleteView, RedirectView, TemplateView, ListView

from datetime import datetime
import os.path

from .models import Event, EventMember
from .forms import CreateEventForm, CreateEventMemberForm
from .utils import ics_to_free_time, possible_time_intervals, time_to_ics


class HomeView(TemplateView):
	template_name = 'core/home.html'


class EventListView(ListView):
	model = Event
	template_name = 'core/listview.html'

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['events'] = Event.objects.all()
	# 	return context

	def get_queryset(self, *args, **kwargs):
		return super(EventListView, self).get_queryset(*args, **kwargs)


class EventCreateView(CreateView):
	"""EventCreateView"""
	template_name = 'core/create.html'
	model = Event
	form_class = CreateEventForm

	def get_success_url(self):
		return self.object.get_absolute_url()

	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def get_form_kwargs(self):
		kwargs = super(EventCreateView, self).get_form_kwargs()
		return kwargs

	def form_invalid(self, form):
		return super().form_invalid(form)

	def form_valid(self, form):
		"""Adds the 'HX-Redirect' header for htmx to redirect to the dashboard"""
		return super().form_valid(form)


class EventDetailView(DetailView):
	"""EventCreateView"""
	template_name = 'core/detail.html'
	model = Event

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = CreateEventMemberForm(event=self.get_object())
		return context

	def get_object(self, queryset=None):
		return Event.objects.get(id=self.kwargs['id'])

	def post(self, request, *args, **kwargs):
		form = CreateEventMemberForm(self.request.POST, self.request.FILES, event=self.get_object())
		if form.is_valid():
			form.save()
		return render(request, self.template_name, {
			'object': self.get_object(),
			'form': form
		})


class ScheduleEventDetailView(DetailView):
	"""ScheduleEventDetailView"""
	template_name = 'core/schedule_detail.html'
	model = Event

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		event = self.get_object()
		filenames = []
		for event_member in event.eventmember_set.all():
			filenames.append(event_member.calendar.path)

		context['free_times'] = collections.OrderedDict(
			sorted(
				possible_time_intervals(
					(event.duration, 0),
					ics_to_free_time(filenames, (event.min_time, 0), (event.max_time, 0))).items()
			)
		)
		return context

	def get_object(self, queryset=None):
		return Event.objects.get(id=self.kwargs['id'])

	def post(self, request, *args, **kwargs):
		event = self.get_object()
		subject = 'Invitation to ' + event.name
		print(request.POST.get('date'))
		html_content = render_to_string('core/email/invitations.html', {
			'event': event,
			'date': request.POST.get('date'),
			'start': request.POST.get('start'),
			'end': request.POST.get('end'),
		})
		text_content = strip_tags(html_content)
		emails = []
		for event_member in event.eventmember_set.all():
			emails.append(event_member.email)

		start_time = tuple(map(int, request.POST.get('start').split(':')))
		end_time = tuple(map(int, request.POST.get('end').split(':')))

		email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_FROM_USER, emails)
		email.attach_alternative(html_content, 'text/html')

		email.attach(
			'event.ics',
			time_to_ics(datetime.strptime(request.POST.get('date'), "%Y-%m-%d"), (start_time, end_time), event.name),
			'text/calendar')
		email.send()

		messages.success(
			self.request,
			json.dumps({
				'data': {
					'title': 'Invites sent',
					'innerHTML': 'You sent out your invitations. Your friends will be notified via email.',
					'type': 'success'
				}
			})
		)
		return super().get(request, *args, **kwargs)


class GoogleCalendarView(RedirectView):
	"""GoogleCalendarView"""
	SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

	def get_redirect_url(self, *args, **kwargs):
		return 'redirect_url'


class EventMemberDeleteView(DeleteView):
	"""RemoveEventMemberView"""
	model = EventMember

	def get_object(self, queryset=None):
		return EventMember.objects.get(id=self.kwargs['id'])

	def get_success_url(self):
		return reverse('core:detail', kwargs={'id': self.object.event.id})

