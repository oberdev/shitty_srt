from utils.task import PeriodicTask, AperiodicTask, Marker
from utils.queue import PriorityQueue
from typing import Callable, List, Dict


def EDF(x: PeriodicTask, y: PeriodicTask):
    if x.count * x.deadline > y.count * y.deadline:
        return 1
    elif x.count * x.deadline < y.count * y.deadline:
        return -1
    else:
        return 0


def RM(x: PeriodicTask, y: PeriodicTask):
    if x.id == y.id:
        if x.exec_time_remaining < y.exec_time_remaining:
            return 1
        elif x.exec_time_remaining > y.exec_time_remaining:
            return -1
        else:
            return 0
    else:
        if x.deadline > y.deadline:
            return 1
        elif x.deadline < y.deadline:
            return -1
        else:
            return 0


class SchedullingService:

    def __init__(self, periodic_tasks: List[PeriodicTask], aperiodic_tasks, hyperperiod_count: int):
        self.periodic_tasks: List[PeriodicTask] = periodic_tasks
        self.aperiodic_tasks: List[AperiodicTask] = aperiodic_tasks
        self.hyperperiod_count: int = hyperperiod_count

    def run(self, method: str):
        pq: PriorityQueue = None
        if method == 'rm':
            pq = PriorityQueue(RM)
        elif method == 'edf':
            pq = PriorityQueue(EDF)
        else:
            return None

        title = f'Алгоритм {method}. Сумарная загруженность {self.sumary_load()}'

        tasks: List[PeriodicTask, AperiodicTask] = self.periodic_tasks + self.aperiodic_tasks
        tasks_out: List[PeriodicTask, AperiodicTask] = []
        total_iters = self.hyper_period()
        for moment in range(total_iters):
            for task in tasks:
                if task.can_spawn(moment):
                    pq.spawn(task, moment)
                    task.recalculate_deadline()
            if pq.peek() is not None:
                pq.peek().execute(moment, pq, lambda x: tasks_out.append(x))

        for task in self.periodic_tasks:
            task.count = 0

        trace = self.trace(tasks_out)
        return title, trace[0], trace[1], None

    def hyper_period(self):
        return self.hyperperiod_count * max([task.deadline for task in self.periodic_tasks])

    def sumary_load(self):
        periodic_load = sum([task.exec_time / task.deadline for task in self.periodic_tasks])
        aperiodic_load = sum([task.exec_time / task.deadline_param for task in self.aperiodic_tasks])
        return periodic_load + aperiodic_load

    def trace(self, tasks: List[PeriodicTask]):
        trace_data: List[dict] = []
        responses: Dict[int, List[Dict[str, int]]] = {task.id: [] for task in tasks}
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
            # Костыль с добавлением одного такта, чтобы дед не вонял
            responses[task.id].append({
                "came_moment": task.stats.came_moment,
                "execute_moment": task.stats.execute_moment,
                "response_time": task.stats.response_time + 1
            })
            trace_data.append({
                "id": task.id,
                "name": task.name,
                "p": task.deadline / 1000,
                "e": task.exec_time / 1000,
                "markers": markers,
                "periods": periods,
            })
        results: Dict[int, List[Dict[str, int]]] = {task.id: {} for task in tasks}
        for key in results:
            temp_responses = [node["response_time"] for node in responses[key]]
            results[key]["max"] = max(temp_responses)
            results[key]["mean"] = sum(temp_responses) / len(temp_responses)
        return trace_data, responses, results
