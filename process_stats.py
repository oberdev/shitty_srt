from openpyxl import Workbook
import json

TASKS_NUM = 13
edf_stats = {}
rm_stats = {}
with open('rm_stats.json') as file:
    rm_stats = json.loads(file.read())
with open('edf_stats.json') as file:
    edf_stats = json.loads(file.read())
print(rm_stats)
wb = Workbook()
ws = wb.active
key = 1
for row in ws.iter_rows(min_row=1, max_row=TASKS_NUM, max_col=4):
    print(row)
    row[0].value  = rm_stats[str(key)]["mean"]
    row[1].value = edf_stats[str(key)]["mean"]
    row[2] .value = rm_stats[str(key)]["max"]
    row[3].value  = edf_stats[str(key)]["max"]
    key +=1

wb.save('stats.xlsx')
