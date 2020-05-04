from typing import List, Callable, Dict
from utils.queue import PriorityQueue
from numpy.random import exponential


class TaskStats:
    def __init__(self):
        self.came_moment = 0
        self.execute_moment = 0
        self.response_time = 0


class Marker:
    def __init__(self, time: int, is_start: bool):
        self.time: int = time
        self.is_start: bool = is_start


class PeriodicTask:

    def __init__(self, id: int, deadline: int, exec_time: int):
        self.id: int = id
        self.deadline: int = deadline
        self.exec_time: int = exec_time
        self.exec_time_remaining: int = exec_time
        self.exec_moments: List[int] = []
        self.count: int = 0
        self.markers: List[Marker] = []
        self.name: str = f'Task {self.id} (p: {self.deadline}, e: {self.exec_time}'
        self.stats: TaskStats = TaskStats()

    def can_spawn(self, moment: int):
        return moment % self.deadline == 0

    def execute(self, moment, pq: PriorityQueue, on_shift: Callable):
        if self.exec_time == self.exec_time_remaining:
            self.stats.execute_moment = moment
            self.markers.append(Marker(
                moment, True
            ))

        self.exec_time_remaining -= 1

        self.exec_moments.append(moment)

        if self.exec_time_remaining == 0:
            pq.shift()
            self.stats.response_time = moment - self.stats.came_moment
            self.markers.append(Marker(
                moment, False
            ))
            on_shift(self)

    def recalculate_deadline(self):
        pass


class AperiodicTask(PeriodicTask):

    def __init__(self, id: int, deadline: int, exec_time: int):
        PeriodicTask.__init__(self, id, deadline, exec_time)
        self.deadline = 0
        self.deadline_param = deadline

    def recalculate_deadline(self):
        self.deadline += int(exponential(self.deadline_param))

    def can_spawn(self, moment: int):
        return moment == self.deadline
