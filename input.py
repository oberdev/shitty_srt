from utils.task import PeriodicTask, ApepiodicTask
from typing import List
import numpy as np
np.random.seed(19)

HYPERPERIODS_COUNT = 1

PERIODIC_TASKS: List[PeriodicTask] = [
    PeriodicTask(1, 60000, 2750),
    PeriodicTask(2, 30000, 7500),
    PeriodicTask(3, 15000, 3000),
    PeriodicTask(4, 20000, 5000)
]

APERIODIC_TASKS = [
    ApepiodicTask(5, 10000, 200),
    ApepiodicTask(6, 20000, 400),
    ApepiodicTask(7, 5000, 150),
    ApepiodicTask(8, 2500, 50),
    ApepiodicTask(9, 1000, 40),
    ApepiodicTask(10, 15000, 300),
    ApepiodicTask(11, 1250, 25),
    ApepiodicTask(12, 30000, 600),
    ApepiodicTask(13, 60000, 1200)
]