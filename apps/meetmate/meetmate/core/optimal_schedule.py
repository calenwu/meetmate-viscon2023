from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Optional

from .models import Calendar

class ScheduleStrategy(ABC):
    @abstractmethod
    def create_schedule(self, input_dict: Dict[int, Calendar], start_time: datetime, deadline: Optional[datetime] = None) -> list:
        pass



class DailySchedule(ScheduleStrategy):
    def create_schedule(self, input_dict: Dict[int, Calendar], start_time: datetime, deadline: Optional[datetime] = None) -> list:
        # TODO
        end_time = deadline or start_time + timedelta(days=7)
        num_slots = input_dict['num_slots']
        duration = (end_time - start_time) / num_slots
        schedule = []
        for i in range(num_slots):
            slot_start = start_time + timedelta(days=i)
            slot_end = slot_start + duration
            schedule.append((slot_start, slot_end))
        return schedule


class WeeklySchedule(ScheduleStrategy):
    def create_schedule(self, input_dict: Dict[int, Calendar], start_time: datetime, deadline: Optional[datetime] = None) -> list:
        # TODO
        end_time = deadline or start_time + timedelta(weeks=4)
        num_slots = input_dict['num_slots']
        duration = (end_time - start_time) / num_slots
        schedule = []
        for i in range(num_slots):
            slot_start = start_time + timedelta(weeks=i)
            slot_end = slot_start + duration
            schedule.append((slot_start, slot_end))
        return schedule


class ScheduleCreator:
    def __init__(self, strategy: ScheduleStrategy):
        self.strategy = strategy

    def create_schedule(self, input_dict: Dict[int, Calendar], start_time: datetime, deadline: Optional[datetime] = None) -> list:
        return self.strategy.create_schedule(input_dict, start_time, deadline)
