from typing import List
from utils.task import PeriodicTask
from services.scheduling import SchedullingService
from flask import Flask
from flask import render_template, jsonify
import json

aperiodic_tasks = []

periodic_tasks: List[PeriodicTask] = [
    PeriodicTask(1, 60000, 2750),
    PeriodicTask(2, 30000, 7500),
    PeriodicTask(3, 15000, 3000),
    PeriodicTask(4, 20000, 5000)
]

app = Flask(__name__)


@app.route("/edf")
def edf():
    title, trace_data, error = SchedullingService(periodic_tasks, aperiodic_tasks).run('edf')
    with open('edf_out.json', 'w') as f:
        json.dump(trace_data, f)
    return render_template("index.html", title=title, trace_data=trace_data)


@app.route("/rm")
def rm():
    title, trace_data, error = SchedullingService(periodic_tasks, aperiodic_tasks).run('rm')
    with open('rm_out.json', 'w') as f:
        json.dump(trace_data, f)
    return render_template("index.html", title=title, trace_data=trace_data)

if __name__ == "__main__":
    app.run()
