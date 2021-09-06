""" Getting base stations placement"""
import json
import time

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
        self.average_packet_size = dataset['average_packet_size']
        self.sta = dataset['sta']


with open('input_new.json') as json_file:
    """
    JSON include input data
    """
    input_dataset = json.load(json_file)
    pd_data = pd.DataFrame(input_dataset)
    pd_data.to_csv('input.csv', sep=';')

    SHARE = 0.007

    for i in range(len(input_dataset)):
        input_data = Problem(input_dataset[i])
        start_time = time.time()
        print(colored('==========OLD ESTIMATE EMETHOD=============',
                      'cyan', attrs=['bold']))
        # output = optimal_solution.get(input_data, SHARE)
        old_est = time.time()
        print('--- OLD ESTIMATE EMETHOD {} seconds ---'.format(old_est -
                                                               start_time))
        print(colored('==========NEW ESTIMATE EMETHOD=============',
                      'cyan', attrs=['bold']))
        output = search.get(input_data, SHARE)
        new_est = time.time()
        print('--- OLD ESTIMATE EMETHOD {} seconds ---'.format(new_est -
                                                               old_est))
