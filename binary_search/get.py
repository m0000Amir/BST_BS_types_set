"""
An optimal problem.
Branch and Bound method using Binary Search Tree.
"""
from network.connection_between_station import is_able_to_exist_solution
from binary_search.tree import Tree, Node
from binary_search.schedule import Schedule
from network.performance_characteristics import solve_cost, solve_delay
from network.performance_characteristics import solve_noncoverage
from network.performance_characteristics import check_delay, check_cost
from network.connection_between_station import check_station_connection
from brute_force.noncoverage import check_noncoverage
from branch_and_bound.noncoverage import check_estimation
from network.link_budget import get_station_parameters

from dataclasses import dataclass

import matlab.engine
import numpy as np
from termcolor import colored


# class Settings:
#     def __init__(self):
#         self.feasible_set_problem = False
#         self.cost_problem = False
#         self.delay_problem = False
#         self.placing_all_station_problem = False


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
        self.relative_deviation = dataset['relative_deviation']
        self.method = dataset['method']


@dataclass()
class InputParameters:
    arrival_rate = None
    average_packet_size = None
    cost_limit = None
    delay_limit = None
    gateway_coordinate = None
    placement_coordinate = None
    cost = None
    throughput = None
    link_distance = None
    link_distance2gateway = None
    coverage = None
    deviation = None
    method = None


def print_placed_station(node: Node, data: dataclass) -> None:
    """
    Print station placement
    Parameters
    ----------
    node - current node
    data - input data

    """
    i, j = np.where(node.left_child.pi == 1)
    placed_sta = ['-'] * len(data.placement_coordinate)

    for k in range(len(i)):
        placed_sta[i[k]] = 'S' + str(j[k] + 1)
    print(colored(placed_sta, 'magenta', 'on_green', attrs=['bold']))


def prepare_problem_data(input_data: Problem) -> InputParameters:
    """

    Parameters
    ----------
    input_data input from JSON-file

    Returns
    -------
        data: InputParameters
    """
    data = InputParameters()

    data.arrival_rate = input_data.arrival_rate
    data.average_packet_size = input_data.average_packet_size
    data.cost_limit = input_data.cost_limit
    data.delay_limit = input_data.delay_limit
    data.gateway_coordinate = input_data.gateway_placement
    data.placement_coordinate = input_data.placement

    data.cost = tuple(input_data.sta[i]['c']
                      for i in range(len(input_data.sta)))
    data.throughput = tuple(
        input_data.sta[i]['throughput'] for i in range(len(input_data.sta)))
    data.link_distance, \
        data.link_distance2gateway, \
        data.coverage = get_station_parameters(input_data.gateway,
                                               input_data.user_device,
                                               input_data.sta)

    relative_deviation = input_data.relative_deviation

    if relative_deviation is None:
        data.deviation = None
    else:
        data.deviation = relative_deviation * (data.gateway_coordinate[1] -
                                               data.gateway_coordinate[0])
    data.method = input_data.method

    return data


def run(input_data: Problem):
    """ Getting problem"""

    data = prepare_problem_data(input_data)

    assert is_able_to_exist_solution(
        data.link_distance,
        data.link_distance2gateway,
        data.placement_coordinate,
        data.gateway_coordinate), 'There is not problem for this case'

    if data.method == 0:
        method = "Branch_and_bound"
        matlab_engine = matlab.engine.start_matlab('-nojvm')
        matlab_engine.cd(r'./branch_and_bound/estimation/matlab/', nargout=0)

    elif data.method == -1:
        method = "Brute_force"
        matlab_engine = None
    else:
        raise ValueError('Error in choosing the problem-solution method. '
                         'Variable 0 means the branch and bound method. '
                         'Variable -1 means the brute force method.')

    """ 
    Starting Searching
    Initialize Tree and Schedule
    """
    tree = Tree()
    tree.initiate(data.placement_coordinate, data.coverage)

    statistics = Schedule(tree.top)
    statistics.record[-1]['optimal'] = data.gateway_coordinate[-1]

    parent = tree.top
    while tree.is_possible_to_add_new_nodes(parent):
        i, j = tree.get_indices(parent.pi)
        if (i is not None) and (j is not None):
            """add left node"""
            tree.add_left_node(i, j, parent)
            parent.left_child.cost = solve_cost(j, parent, data)
            parent.left_child.delay = solve_delay(j, parent, data)
            left_noncoverage, right_noncoverage = solve_noncoverage(
                i, j, parent, data)
            parent.left_child.noncoverage.left = left_noncoverage
            parent.left_child.noncoverage.right = right_noncoverage

            """add right node"""
            tree.add_right_node(i, j, parent)
            parent.right_child.noncoverage = parent.noncoverage
            parent.right_child.cost = parent.cost
            parent.right_child.delay = parent.delay

            # PLOT GRAPH
            # draw(tree.graph)

            if (check_station_connection(i, j, parent, data)
                    and check_cost(parent.left_child, data.cost_limit)
                    and check_delay(parent.left_child, data.delay_limit)):
                if method == "Branch_and_bound":
                    "Branch and bound method"
                    if check_estimation(i, j, parent, data, statistics,
                                        matlab_engine):
                        parent = parent.left_child
                    else:
                        tree.unchecked_node.pop()
                        parent = parent.right_child
                else:
                    "Brute force method"
                    check_noncoverage(i, j, parent, data, statistics)
                    parent = parent.left_child
            else:
                tree.unchecked_node.pop()
                parent = parent.right_child
        else:
            parent = tree.unchecked_node[-1]
            tree.unchecked_node.pop()
        # draw(tree.graph)
    print('Total number of nodes is {}'.format(tree.node_keys[-1]))
