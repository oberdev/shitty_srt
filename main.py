from services.scheduling import SchedullingService
from flask import Flask, Markup
from flask import render_template, jsonify
import json
from input import PERIODIC_TASKS, APERIODIC_TASKS, HYPERPERIODS_COUNT
from copy import deepcopy


app = Flask(__name__)


@app.route("/edf")
def edf():
    title, trace_data, responses, error = SchedullingService(PERIODIC_TASKS, deepcopy(APERIODIC_TASKS), HYPERPERIODS_COUNT).run('edf')
    with open('edf_out.json', 'w') as f:
        json.dump(trace_data, f)
    return render_template("index.html", title=title, trace_data=Markup(trace_data))


@app.route("/rm")
def rm():
    title, trace_data, responses, error = SchedullingService(PERIODIC_TASKS, deepcopy(APERIODIC_TASKS), HYPERPERIODS_COUNT).run('rm')
    with open('rm_out.json', 'w') as f:
        json.dump(trace_data, f)
    return render_template("index.html", title=title, trace_data=Markup(trace_data))


if __name__ == "__main__":
    app.run()
