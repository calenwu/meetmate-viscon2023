import datetime
from django import template

register = template.Library()


@register.simple_tag()
def two_digits(number: int) -> str:
	if number >= 10:
		return str(number)
	return '0' + str(number)


@register.simple_tag()
def format_date(date: datetime) -> str:
	return date.date().strftime("%A, %d. %B")


@register.simple_tag()
def format_date_string(date: str) -> str:
	return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d. %B")


@register.simple_tag()
def get_date(date: datetime) -> str:
	return date.date()
