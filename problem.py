""" Getting base stations placement"""
import json
import time

from termcolor import colored

from binary_search.nodes import get_nodes_number
from binary_search import get
from binary_search.get import Problem


with open('config.json') as json_file:
    """
    JSON include input data
    """
    config = json.load(json_file)


with open('input/article_experience4.json') as json_file:
    """
    JSON include input data
    """
    input_dataset = json.load(json_file)

    input_data = Problem(input_dataset)
    start_time = time.time()
    get.run(input_data, config)
    new_est = time.time()
    get_nodes_number(input_dataset)
    print(colored(f'--- ESTIMATE TIME {new_est - start_time} seconds ---',
                  'cyan', attrs=['bold']))
