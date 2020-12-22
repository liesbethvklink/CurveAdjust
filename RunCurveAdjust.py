import csv
import sys
import copy

#System settings
sys.setrecursionlimit(10000)

#Global settings
input_file = 'input.csv'
col_num = 3

#Elenrgy settings
capacity = 17400000.0
max_h = 7300.0

#Variables
CSV_Values = []
s_list = []
rem_c = float(capacity)
app_c = {}

#Functions
def PerformAdjustment(i):
    global rem_c  # Global Fix
    global s_list #Global Fix
    if(i >= len(s_list)) : dt_neighbour = max_h #Last item fix
    elif(s_list[i]["value"] >= 0) : dt_neighbour = s_list[i]["value"] #Upper boundry fix
    else : dt_neighbour = abs(s_list[i]["value"]) - abs(s_list[i + 1]["value"])

    dt = s_list[i]["dt"]
    if dt in app_c.keys() : max_applicable = max_h - app_c[dt]
    else : max_applicable = max_h
    max_applicable = min(max_applicable, rem_c, abs(s_list[i]["value"]))

    applied = min(max_applicable, dt_neighbour)
    if dt in app_c.keys() : app_c[dt] += applied
    else : app_c[dt] = applied

    rem_c += -applied

    s_list[i]["value"] = s_list[i]["value"] + applied
    if(max_applicable > 0) :
        if(i > 0) :
            PerformAdjustment(i - 1)

#Process the input file
with open(input_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            CSV_Values.append({
                'dt' : line_count - 1,
                'value' : float(row[col_num])
            })
        line_count += 1
#Sort the CSV Values list by the value.
s_list = copy.deepcopy(CSV_Values)
s_list = sorted(s_list, key=lambda i: i['value'])

#Run an iterative function on the sorted list
key = -1
for dict in s_list:
    key += 1
    if rem_c <= 0 : continue
    if dict.get("value") >= 0 : continue

    PerformAdjustment(key)
f_list = copy.deepcopy(s_list)
f_list = sorted(f_list, key=lambda i: i['dt'])

#Write the results to the output file
with open('output.csv', mode='w', newline='') as csv_file:
    csv_file.truncate()
    fieldnames = ['new_value']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #writer.writeheader()
    for key in range(len(f_list)):
        row = {}
        row["new_value"] = f_list[key]["value"]
        writer.writerow(row)

