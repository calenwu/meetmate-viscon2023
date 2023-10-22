from django import forms
from .models import Event, EventMember


class CreateEventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['name', 'description', 'duration', 'min_time', 'max_time', 'location']

	def __init__(self, *args, **kwargs):
		super(CreateEventForm, self).__init__(*args, **kwargs)


class CreateEventMemberForm(forms.ModelForm):
	class Meta:
		model = EventMember
		fields = ['name', 'email', 'calendar']

	def __init__(self, *args, **kwargs):
		self.event = kwargs.pop('event', None)
		super(CreateEventMemberForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		instance = super(CreateEventMemberForm, self).save(commit=False)
		# Set the event field
		instance.event = self.event
		if commit:
			instance.save()
		return instance
