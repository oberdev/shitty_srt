from services.scheduling import SchedullingService
from flask import Flask, Markup
from flask import render_template, jsonify
import json
from input import PERIODIC_TASKS, APERIODIC_TASKS, HYPERPERIODS_COUNT
from copy import deepcopy
from docx import Document


def create_tables_trace(document_name, trace):
    document = Document()
    for key in range(1, len(PERIODIC_TASKS + APERIODIC_TASKS) + 1):
        document.add_heading(f'Задача №{key}', level=1)
        table = document.add_table(rows=1, cols=4)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Номер вызова'
        hdr_cells[1].text = 'Время вызова'
        hdr_cells[2].text = 'Время запуска'
        hdr_cells[3].text = 'Время отклика'
        for task_num, task_trace in enumerate(trace[key]):
            row_cells = table.add_row().cells
            row_cells[0].text = str(task_num+1)
            row_cells[1].text = str(task_trace['came_moment']/1000)
            row_cells[2].text = str(task_trace['execute_moment']/1000)
            row_cells[3].text = str(task_trace['response_time']/1000)
        document.add_page_break()

    document.save(f'{document_name}.docx')


app = Flask(__name__)


@app.route("/edf")
def edf():
    title, trace_data, responses, error = SchedullingService(PERIODIC_TASKS, deepcopy(APERIODIC_TASKS),
                                                             HYPERPERIODS_COUNT).run('edf')
    create_tables_trace('edf', responses)
    with open('edf_out.json', 'w') as f:
        json.dump(trace_data, f)
    return render_template("index.html", title=title, trace_data=Markup(trace_data))


@app.route("/rm")
def rm():
    title, trace_data, responses, error = SchedullingService(PERIODIC_TASKS, deepcopy(APERIODIC_TASKS),
                                                             HYPERPERIODS_COUNT).run('rm')
    create_tables_trace('rm', responses)
    with open('rm_out.json', 'w') as f:
        json.dump(trace_data, f)
    return render_template("index.html", title=title, trace_data=Markup(trace_data))


if __name__ == "__main__":
    app.run()
