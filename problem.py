""" Getting base stations placement"""
import json
import time

import pandas as pd
from termcolor import colored

from binary_search import get
from binary_search.get import Problem


with open('input_brute_force.json') as json_file:
    """
    JSON include input data
    """
    input_dataset = json.load(json_file)
    pd_data = pd.DataFrame(input_dataset)
    pd_data.to_csv('input.csv', sep=';')

    for i in range(len(input_dataset)):
        input_data = Problem(input_dataset[i])
        start_time = time.time()
        output = get.run(input_data)
        new_est = time.time()
        print(colored(f'--- ESTIMATE TIME {new_est - start_time} seconds ---',
                      'cyan', attrs=['bold']))
