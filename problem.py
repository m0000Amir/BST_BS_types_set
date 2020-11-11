""" Getting base stations placement"""
import json


import pandas as pd
from termcolor import colored

from solution import optimal_solution, search


class Problem:
    """
    Input Data of Placement Problem

    We have points of placements and gateways. Packets are described arival
    rate.
    """
    def __init__(self, dataset):
        self.placement = tuple(dataset['placement'])
        self.gateway_placement = tuple(dataset['gateway_placement'])
        self.gateway = dataset['gateway']
        self.user_device = dataset['user_device']
        self.cost_limit = dataset['cost_limit']
        self.delay_limit = dataset['delay_limit']
        self.arrival_rate = dataset['arrival_rate']
        self.sta = dataset['sta']


with open('input.json') as json_file:
    """
    JSON include input data
    """
    input_dataset = json.load(json_file)
    pd_data = pd.DataFrame(input_dataset)
    pd_data.to_csv('input.csv', sep=';')

    SHARE = 0.1

    for i in input_dataset.keys():
        input_data = Problem(input_dataset[i])
        # print(colored('==========OLD ESTIMATE EMETHOD=============',
        #               'cyan', attrs=['bold']))
        # output = optimal_solution.get(input_data, SHARE)
        print(colored('==========NEW ESTIMATE EMETHOD=============',
                      'cyan', attrs=['bold']))
        output = search.get(input_data, SHARE)
