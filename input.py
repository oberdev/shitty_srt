from utils.task import PeriodicTask
from typing import List

HYPERPERIODS_COUNT = 1

PERIODIC_TASKS: List[PeriodicTask] = [
    PeriodicTask(1, 60000, 2750),
    PeriodicTask(2, 30000, 7500),
    PeriodicTask(3, 15000, 3000),
    PeriodicTask(4, 20000, 5000)
]

APERIODIC_TASKS = []