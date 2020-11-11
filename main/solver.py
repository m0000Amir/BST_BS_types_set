"""
Input data for binary search tree
"""
import json
import csv

import pandas as pd

from main.bab import BST
from main.figure import draw

with open('data.json') as json_file:
    data = json.load(json_file)

pd_data = pd.DataFrame(data)
pd_data.to_csv('input.csv', sep=';')
# outputFile = open('input.csv', 'w')
# output = csv.writer(outputFile)  # create a csv.write
# output.writerow(data)

solution_result = list()

for i in data.keys():
    placement = data[i]['placement']
    gateway_placement = data[i]['gateway_placement']
    cost_limit = data[i]['cost_limit']
    delay_limit = data[i]['delay_limit']
    arrival_rate = data[i]['arrival_rate']

    sta = data[i]['sta']

    solution = BST(placement, gateway_placement, cost_limit, delay_limit, sta,
                   arrival_rate)
    solution.search()
    # draw(solution.graph)

    print('record =  ', solution.table.record[-1],
          ',  Number of nodes = ', len(solution.nodes))

    solution_result.append(solution.table.print_record[-1])

# writing to csv file
with open('output.csv', 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)

    # writing the fields
    csvwriter.writerow(['output_BaB'])
    for raw in solution_result:
        csvwriter.writerow([raw])




