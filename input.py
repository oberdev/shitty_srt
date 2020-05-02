from utils.task import PeriodicTask, AperiodicTask
from typing import List
import numpy as np
np.random.seed(1)

HYPERPERIODS_COUNT = 4

PERIODIC_TASKS: List[PeriodicTask] = [
    PeriodicTask(1, 60000, 2750),
    PeriodicTask(2, 30000, 7500),
    PeriodicTask(3, 15000, 3000),
    PeriodicTask(4, 20000, 5000)
]

APERIODIC_TASKS = [
    AperiodicTask(5, 10000, 200),
    AperiodicTask(6, 20000, 400),
    AperiodicTask(7, 5000, 150),
    AperiodicTask(8, 2500, 50),
    AperiodicTask(9, 1000, 40),
    AperiodicTask(10, 15000, 300),
    AperiodicTask(11, 1250, 25),
    AperiodicTask(12, 30000, 600),
    AperiodicTask(13, 60000, 1200)
]