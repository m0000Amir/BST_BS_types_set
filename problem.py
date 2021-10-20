""" Getting base stations placement"""
import json
import time

import pandas as pd
from termcolor import colored

from binary_search import get


class Problem:
    """
    Input Data of Placement Problem

    We have points of placements and gateways. Packets are described arrival
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

    SHARE = 0.005
    SHARE = None

    for i in range(len(input_dataset)):
        input_data = Problem(input_dataset[i])
        start_time = time.time()
        output = get.run(input_data, SHARE)
        new_est = time.time()
        print(colored(f'--- ESTIMATE TIME {new_est - start_time} seconds ---',
                      'cyan', attrs=['bold']))
