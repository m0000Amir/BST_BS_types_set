""" Getting base stations placement"""
import json
import time

from termcolor import colored

from binary_search import get
from binary_search.get import Problem


with open('config.json') as json_file:
    """
    JSON include input data
    """
    config = json.load(json_file)


with open('input_new.json') as json_file:
    """
    JSON include input data
    """
    input_dataset = json.load(json_file)

    for i in range(len(input_dataset)):
        input_data = Problem(input_dataset[i])
        start_time = time.time()
        get.run(input_data, config)
        new_est = time.time()
        print(colored(f'--- ESTIMATE TIME {new_est - start_time} seconds ---',
                      'cyan', attrs=['bold']))
