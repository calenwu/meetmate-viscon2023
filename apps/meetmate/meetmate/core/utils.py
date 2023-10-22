import uuid
import hashlib
import base64
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import gettext as _
from http import HTTPStatus
from sys import platform as os

from ics import Calendar, Event
from datetime import datetime
from datetime import timedelta

passkey = 'asdf'

non_float_currs = [
	"JPY"
]


def weekday():
	return {
		0: _('Monday'),
		1: _('Tuesday'),
		2: _('Wednesday'),
		3: _('Thursday'),
		4: _('Friday'),
		5: _('Saturday'),
		6: _('Sunday'),
	}


def two_digits(num: int) -> str:
	if num < 10:
		return '0' + str(num)
	return str(num)


def encrypt_string(string: str) -> str:
	enc = []
	for i in range(len(string)):
		key_c = passkey[i % len(passkey)]
		enc_c = chr((ord(string[i]) + ord(key_c)) % 256)
		enc.append(enc_c)
	return base64.urlsafe_b64encode(''.join(enc).encode()).decode().replace('=', 'tamadebukeneng192khs').replace('+',
	                                                                                                             'wobuzhidao3810tmds')


def decrypt_string(string: str) -> str:
	dec = []
	enc = base64.urlsafe_b64decode(
		string.replace('tamadebukeneng192khs', '=').replace('wobuzhidao3810tmds', '+')).decode()
	for i in range(len(enc)):
		key_c = passkey[i % len(passkey)]
		dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
		dec.append(dec_c)
	return ''.join(dec)


def concat_form_errors(form_errors):
	all_errors = ''
	temp = list(form_errors.values())
	for error in form_errors.values():
		for err in error:
			all_errors += err
			if error != temp[-1] and err != error[-1]:
				all_errors += '\n'
	return all_errors


def add_middleware_to_request(request, middleware_class):
	middleware = middleware_class(request)
	middleware.process_request(request)
	return request


# def add_middleware_to_response(request, middleware_class):
# 	middleware = middleware_class()
# 	middleware.process_response(request)
# 	return request


def remove_attribute(driver, attribute: str, css_selector: str) -> None:
	driver.execute_script('arguments[0].removeAttribute("' + attribute + '")', get_element(driver, css_selector))


def set_value(driver, value: str, css_selector: str) -> None:
	driver.execute_script('arguments[0].value = "' + value + '";', get_element(driver, css_selector))


def hx_redirect(http_response: HttpResponse, url: str) -> HttpResponse:
	"""Adds a 'HX-Redirect' to the HttpResponse and changes the status_code to 200"""
	http_response.headers['HX-Redirect'] = url
	http_response.status_code = HTTPStatus.OK
	return http_response


def hx_trigger(http_response: HttpResponse, event: str) -> HttpResponse:
	"""Adds a 'HX-Trigger' to the HttpResponse and changes the status_code to 200"""
	http_response.headers['HX-Trigger'] = event
	http_response.status_code = HTTPStatus.OK
	return http_response


def decimal_amount(currency: str, amount: float) -> float:
	if currency in non_float_currs:
		return amount
	return amount / 100


def decimal_amount_str(currency: str, amount: float):
	if currency in non_float_currs:
		return str(amount)
	return print_2_decimals(amount / 100)


def print_2_decimals(val) -> str:
	return '{:.2f}'.format(val)


def convert_to_real_price(currency: str, price: int) -> float:
	if currency in non_float_currs:
		return price
	return price / 100.0


def convert_to_smallest_unit(currency: str, price: int) -> float:
	if currency in non_float_currs:
		return price
	return price * 100.0


def generate_long_id():
	# Create two random UUIDs
	uuid1 = uuid.uuid4()
	uuid2 = uuid.uuid4()

	# Combine and hash them
	combined = f"{uuid1}{uuid2}"
	hashed_id = hashlib.sha256(combined.encode()).hexdigest()
	return hashed_id


def same_day(begin, end):
	return begin.year == end.year and begin.month == end.month and begin.day == end.day


def parse_blockedtimes(filename='Benjamin Horner Calendar.ics'):
	"""
  Outlook calendar export has all the non-free events.
  event.name: Busy, Working elsewhere (not contained: free)
  event.begin: 2023-10-20T13:00:00+00:00
  event.end:

  output: dictionary mapping date to list of sorted events (tuples (hrs, min):(int, int) for start and end)

  """
	with open(filename, 'r', encoding='utf-8') as f:
		ics_data = f.read()

	c = Calendar(ics_data)
	date_format = "%Y-%m-%dT%H:%M:%S%z"

	sorted_events = sorted(c.events, key=lambda event: event.begin)  # not really needed here

	# multi-day events: split up events where end date != begin date
	new_events = {}
	for event in sorted_events:
		if "free" in (event.name).lower():
			continue
		begin = datetime.strptime(str(event.begin), date_format)
		end = datetime.strptime(str(event.end), date_format)

		if not same_day(begin, end):
			date_begin = datetime(begin.year, begin.month, begin.day)
			date_end = datetime(end.year, end.month, end.day)
			time_tuple = ((begin.hour, begin.minute), (end.hour, end.minute))
			cur_date = date_begin
			cur_time = time_tuple[0]
			while (cur_date < date_end):
				t = (cur_time, (24, 0))  # to check
				if cur_date in new_events:
					new_events[cur_date].append(t)
				else:
					new_events[cur_date] = [t]
				cur_date += timedelta(days=1)
				cur_time = (0, 0)  # to check
			if cur_date == date_end:
				t = (cur_time, time_tuple[1])  # to check
				if cur_date in new_events:
					new_events[cur_date].append(t)
				else:
					new_events[cur_date] = [t]

	# single-day events
	blocked_times = {}
	for event in sorted_events:
		if "free" in (event.name).lower():
			continue
		begin = datetime.strptime(str(event.begin), date_format)
		end = datetime.strptime(str(event.end), date_format)

		if same_day(begin, end):
			date = datetime(begin.year, begin.month, begin.day)
			time_tuple = ((begin.hour, begin.minute), (end.hour, end.minute))
			if date in blocked_times:
				blocked_times[date].append(time_tuple)
			else:
				blocked_times[date] = [time_tuple]
		else:
			continue

	# merge new partitioned events into complete list
	for date in new_events:
		if date in blocked_times:
			blocked_times[date].extend(new_events[date])
		else:
			blocked_times[date] = new_events[date]
	# sort the merged datastructure
	complete_sorted = {}
	for date in blocked_times:
		complete_sorted[date] = sorted(blocked_times[date], key=lambda elem: elem[0])

	# complete_sort = dict(sorted(complete_sort.items())) TODO tried to sort according to date

	return complete_sorted


def get_free_times_from_blocked_times(blocked_times, time_begin, time_end):
	"""
  Require: list of times is sorted by beginning time
  """
	free_times = {}
	for date in blocked_times:
		times_list = blocked_times[date]
		cur = time_begin

		for i in times_list:
			if i[0] < cur and i[1] <= cur:
				continue
			elif i[0] <= cur:
				cur = i[1]
			elif time_end <= i[1]:  # blocked until after end time
				break
			else:  # there is some free time
				if date in free_times:
					free_times[date].append((cur, i[0]))
				else:
					free_times[date] = [(cur, i[0])]
				cur = i[1]
		if cur < time_end:  # add the last remaining free time
			if date in free_times:
				free_times[date].append((cur, time_end))
			else:
				free_times[date] = [(cur, time_end)]
	return free_times


def compute_intersection(time1, time2):
	intersection_start = max(time1[0], time2[0])
	intersection_end = min(time1[1], time2[1])
	return (intersection_start, intersection_end)


def detect_free_time(persons):
	"""
  Evaluation without considering the day
  input: [ [ (,) ] ] for every person an array of time slots
  output: [ (,) ] an array of intersecting free time slots
  """
	result_calender = persons[0]
	for curr in persons[1:]:
		new_result_calendar = []
		i = j = 0
		while (i < len(result_calender) and j < len(curr)):
			if (result_calender[i][1] < curr[j][0]):
				i += 1
			elif (curr[j][1] < result_calender[i][0]):
				j += 1
			else:

				new_result_calendar.append(compute_intersection(result_calender[i], curr[j]))
				if (result_calender[i][1] < curr[j][1]):
					i += 1
				else:
					j += 1
		result_calender = new_result_calendar
	return result_calender


def ics_to_free_time_content(array_ics, min_t=(6,0), max_t=(22,0)):
	d = {}
	for ics in array_ics:
		x = get_free_times_from_blocked_times(parse_blockedtimes(str(ics)), min_t, max_t)
		for date in x:
			if date in d:
				d[date].append(x[date])
			else:
				d[date] = [x[date]]
	sol = {}
	for date in d:
		sol[date] = detect_free_time(d[date])
	return sol


def ics_to_free_time(array_ics, min_t=(6,0), max_t=(22,0)):
	sol = ics_to_free_time_content(array_ics, min_t, max_t)
	i = 0
	while len(sol.keys()) == 0:
		i += 1
		sol = ics_to_free_time_content(array_ics[i:], min_t, max_t)
	return sol


def possible_time_intervals(duration, d):
	sol = {}
	for date in d:
		if d[date] is None:
			continue
		for t in d[date]:
			t1 = t[0]
			t2 = t[1]
			minutes_t1 = t1[0] * 60 + t1[1]
			minutes_t2 = t2[0] * 60 + t2[1]
			minutes_duration = duration[0] * 60 + duration[1]
			if minutes_t2 - minutes_t1 >= minutes_duration:
				if date in sol:
					sol[date].append((t1, (t1[0] + duration[0], t1[1] + duration[1])))
				else:
					sol[date] = [(t1, (t1[0] + duration[0], t1[1] + duration[1]))]
	return sol


def time_to_ics(date, time, event_name):
	cal = Calendar()
	event = Event()
	event_date_begin = datetime(date.year, date.month, date.day, time[0][0], time[0][1])
	event.begin = event_date_begin
	event_date_end = datetime(date.year, date.month, date.day, time[1][0], time[1][1])
	event.end = event_date_end
	event.name = event_name

	cal.events.add(event)

	cal.events.add(event)
	ics_data = str(cal)

	return ics_data
	# ics_data = str(cal)
	# # Define the filename for the ICS file
	# ics_filename = "my_calendar.ics"
	#
	# # Save the ICS data to a file
	# with open(ics_filename, "w") as ics_file:
	# 	ics_file.write(ics_data)
