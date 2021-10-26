import json
from math import factorial


def get_nodes_number(input_dataset: dict) -> None:
    """
    Get all number of placement of stations

    Parameters
    ----------
    input_dataset: dict

    Returns
    -------

    """

    n = len(input_dataset['placement'])
    m = len(input_dataset['sta'])

    print(f'Placement number = {n}')
    print(f'Station number = {m}')
    result = (factorial(n)/(factorial(n-m) * factorial(m))) * factorial(m)
    print(f'Number of feasible placement = {result}')


if __name__ == "__main__":
    with open('../input_new.json') as json_file:
        """
        JSON include input data
        """
        input_dataset = json.load(json_file)
        get_nodes_number(input_dataset)
