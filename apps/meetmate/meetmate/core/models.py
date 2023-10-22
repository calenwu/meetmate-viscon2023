from django.db import models
from django.urls import reverse
from .utils import generate_long_id


class Event(models.Model):
	id = models.CharField(max_length=64, primary_key=True, default=generate_long_id, editable=False)
	name = models.CharField(max_length=255)
	description = models.TextField(null=True, blank=True)
	duration = models.IntegerField()
	min_time = models.IntegerField()
	max_time = models.IntegerField()
	location = models.CharField(max_length=255)

	def get_absolute_url(self):
		return reverse('core:detail', kwargs={'id': self.id})


class EventMember(models.Model):
	id = models.CharField(max_length=64, primary_key=True, default=generate_long_id, editable=False)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	email = models.EmailField()
	calendar = models.FileField(upload_to='calendar')


class Calendar(models.Model):
	id = models.CharField(max_length=64, primary_key=True, default=generate_long_id, editable=False)
	calendar = models.FileField(upload_to='calendar')
	preferences = ...
	
	@property
	def get_events(self):
		# TODO
		pass
