from utils.task import PeriodicTask, Marker
from utils.queue import PriorityQueue
from typing import Callable, List, Dict
from copy import deepcopy


def EDF(x: PeriodicTask, y: PeriodicTask):
    if x.count * x.period > y.count * y.period:
        return 1
    elif x.count * x.period < y.count * y.period:
        return -1
    else:
        return 0


def RM(x: PeriodicTask, y: PeriodicTask):
    if x.id == y.id:
        if x.exec_time_remaining > y.exec_time_remaining:
            return 1
        elif x.exec_time_remaining < y.exec_time_remaining:
            return -1
        else:
            return 0
    else:
        if x.period < y.period:
            return 1
        elif x.period > y.period:
            return -1
        else:
            return 0


class SchedullingService:

    def __init__(self, periodic_tasks: List[PeriodicTask], aperiodic_tasks):
        self.periodic_tasks: List[PeriodicTask] = periodic_tasks
        self.aperiodic_tasks: List = aperiodic_tasks

    def run(self, method: str):
        pq: PriorityQueue = None
        if method == 'rm':
            pq = PriorityQueue(RM)
        elif method == 'edf':
            pq = PriorityQueue(EDF)
        else:
            return None

        periodic_tasks_out: List[PeriodicTask] = []
        total_iters = self.hyper_period()
        for moment in range(total_iters):
            for task in self.periodic_tasks:
                if task.can_spawn(moment):
                    spawn(task, pq)

            if pq.peek() != None:
                pq.peek().execute(moment, pq, lambda x: periodic_tasks_out.append(x))

        for task in self.periodic_tasks:
            task.count = 0

        title = f'Алгоритм {method}. Сумарная загруженность {self.sumary_load()}'

        return title, self.trace(periodic_tasks_out), None

    def hyper_period(self):
        return max([task.period for task in self.periodic_tasks])

    def sumary_load(self):
        periodic_load = sum([task.exec_time / task.period for task in self.periodic_tasks])
        return periodic_load

    def trace(self, tasks: List[PeriodicTask]):
        trace_data: List[dict] = []
        for task in tasks:
            markers: List[dict] = []
            for marker in task.markers:
                marker_data = {
                    "type": "diamond",
                    "value": marker.time
                }
                if not marker.is_start:
                    marker_data["fill"] = "#FF0000"
                markers.append(marker_data)
            periods: List[Dict[str, int]] = []
            for exec_moment in task.exec_moments:
                if len(periods) > 0:
                    last = periods[-1]
                    if exec_moment - last["end"] == 1:
                        last["end"] = exec_moment
                        continue
                periods.append({
                    "start": exec_moment,
                    "end": exec_moment
                })
            trace_data.append({
                "id": task.id,
                "name": task.name,
                "p": task.period / 1000,
                "e": task.exec_time / 1000,
                "markers": markers,
                "periods": periods,
            })
        return trace_data


def spawn(task: PeriodicTask, pq: PriorityQueue):
    task.count += 1
    instance = deepcopy(task)
    pq.add(instance)
