from typing import List, Callable
from utils.queue import PriorityQueue


class Marker:
    def __init__(self, time: int, is_start: bool):
        self.time: int = time
        self.is_start: bool = is_start


class PeriodicTask:

    def __init__(self, id: int, period: int, exec_time: int):
        self.id: int = id
        self.period: int = period
        self.exec_time: int = exec_time
        self.exec_time_remaining: int = exec_time
        self.exec_moments: List[int] = []
        self.count: int = 0
        self.markers: List[Marker] = []
        self.name: str = f'Задача №{self.id} (p: {self.period}, e: {self.exec_time}'

    def can_spawn(self, moment: int):
        return moment % self.period == 0

    def execute(self, moment, pq: PriorityQueue, on_shift: Callable):
        if self.exec_time == self.exec_time_remaining:
            self.markers.append(Marker(
                moment, True
            ))

        self.exec_time_remaining -= 1

        self.exec_moments.append(moment)

        if self.exec_time_remaining == 0:
            pq.shift()
            self.markers.append(Marker(
                moment, False
            ))
            on_shift(self)
