from typing import Callable, List
from functools import cmp_to_key
from copy import deepcopy

Comparator = Callable[[int, int], bool]
PQArray = List


class PriorityQueue:
    def __init__(self, comparator: Comparator):
        self.comparator: Comparator = comparator
        self.array: PQArray = []

    def get(self, i: int):
        return self.array[i]

    def add(self, x: dict):
        self.array.append(x)
        self.array.sort(key=cmp_to_key(self.comparator))

    def peek(self):
        if self.length() == 0:
            return None
        else:
            return self.array[0]

    def shift(self):
        if self.length() == 0:
            return None
        else:
            return self.array.pop(0)

    def length(self):
        return len(self.array)

    def spawn(self, task, moment: int):
        task.count += 1
        instance = deepcopy(task)
        instance.stats.came_moment = moment
        self.add(instance)


class AperiodicQueue(PriorityQueue):

    def spawn(self, task, moment: int):
        PriorityQueue.spawn(self, task, moment)
        task.recalculate_apear_time()
