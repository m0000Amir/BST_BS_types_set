""" Getting base stations placement"""
import json
import time

from termcolor import colored

from binary_search import get


with open('input/article_experience4_debug.json') as json_file:
    """
    JSON include input data
    """
    input_dataset = json.load(json_file)

    start_time = time.time()
    get.run(input_dataset)
    new_est = time.time()
    print(colored(f'--- ESTIMATION TIME {new_est - start_time} seconds ---',
                  'cyan', attrs=['bold']))
