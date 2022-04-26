"""
An optimal placement problem.
Branch and Bound method using Binary Search Tree.
"""
from dataclasses import dataclass
from math import factorial

from bsoppy.network.connection_between_station import is_able_to_exist_solution
from bsoppy.binary_search.tree import Tree, Node
from bsoppy.binary_search.schedule import Schedule
from bsoppy.network.performance_characteristics import solve_cost, solve_delay
from bsoppy.network.performance_characteristics import solve_noncoverage
from bsoppy.network.performance_characteristics import check_delay, check_cost
from bsoppy.network.connection_between_station import check_able_to_connect_station
from bsoppy.network.connection_between_station import is_able_to_connect_gateways
from bsoppy.brute_force.noncoverage import check_noncoverage
from bsoppy.branch_and_bound.noncoverage import check_estimation
from bsoppy.network.link_budget import get_station_parameters
from bsoppy.drawing.figure import plot

import numpy as np


@dataclass()
class Restriction:
    cost_limit: None
    delay_limit: None


@dataclass()
class Arrival:
    rate: None
    packet_size: None


@dataclass()
class Configuration:
    method: None
    place_all_station: None
    estimation_method: None
    deviation: None
    last_optimal_noncoverage: None
    drawing: None


@dataclass()
class Radio:
    sta = None
    gateway = None
    user_device = None
    frequency = None
    link_som = None
    coverage_som = None
    link_distance = None
    link_distance2gateway = None
    gateway2link_distance = None
    coverage = None


@dataclass()
class InputData:
    configuration = Configuration
    gateway_coordinate = None
    placement_coordinate = None
    restriction = Restriction
    arrival = Arrival
    cost = None
    throughput = None
    radio = Radio


def prepare(input_dataset: dict) -> InputData:
    """
    Preparation of problem input data

    Parameters
    ----------
    input_dataset - dict() from JSON-file

    Returns
    -------
        data: InputData
    """
    data = InputData()

    # Given coordinates
    data.gateway_coordinate = tuple(input_dataset['gateway_placement'])
    data.placement_coordinate = tuple(input_dataset['placement'])

    # Configuration of the problem
    data.configuration.method = input_dataset["configuration"]["method"]
    data.configuration.place_all_station = (
        input_dataset["configuration"]["place_all_station"])
    data.configuration.estimation_method = (
        input_dataset["configuration"]["estimation_method"])
    data.configuration.deviation = (
        input_dataset["configuration"]["relative_deviation"] * (
            data.gateway_coordinate[1] - data.gateway_coordinate[0])
        if input_dataset["configuration"]["relative_deviation"] else None)
    data.configuration.last_optimal_noncoverage = (
        input_dataset["configuration"]["last_optimal_noncoverage"])
    data.configuration.drawing = input_dataset["configuration"]["drawing"]

    # Exceptions
    method = ["bf", "bab"]  # `brute force` and `branch and bound`
    if data.configuration.method not in method:
        raise ValueError('Wrong method of solving the problem.'
                         'Choose bf or bnb')

    estimation_method = ["ILP", 'knapsack', 'LP']
    if data.configuration.estimation_method not in estimation_method:
        raise ValueError('Wrong method of solving right estimation coverage of '
                         'in branch and bound method.'
                         'Choose ILP, knapsack or LP.')

    if data.configuration.deviation is not None:
        assert data.configuration.last_optimal_noncoverage is not None, \
            "Input data consist relative deviation."
        "It is necessary to give last found optimal noncoverage."

    # Given restriction of the problem
    data.restriction.delay_limit = input_dataset['delay_limit']
    data.restriction.cost_limit = input_dataset['cost_limit']

    # Given arrival parameters
    data.arrival.rate = input_dataset['arrival_rate']
    data.arrival.packet_size = input_dataset['average_packet_size']

    # Given cost and throughput of stations
    data.cost = tuple(input_dataset["sta"][i]['cost']
                      for i in range(len(input_dataset["sta"])))
    data.throughput = tuple(input_dataset["sta"][i]['throughput']
                            for i in range(len(input_dataset["sta"])))

    # Radio communication parameters
    data.radio.sta = input_dataset["sta"]
    data.radio.gateway = input_dataset["gateway"]
    data.radio.user_device = input_dataset['user_device']
    data.radio.frequency = input_dataset["frequency"]
    data.radio.link_som = input_dataset["link_som"]
    data.radio.coverage_som = input_dataset["coverage_som"]

    ld, l2g, g2l, cov,  = get_station_parameters(
        gateway=data.radio.gateway,
        user_device=data.radio.user_device,
        sta=data.radio.sta,
        f=data.radio.frequency,
        link_som=data.radio.link_som,
        coverage_som=data.radio.coverage_som)
    data.radio.coverage = cov
    data.radio.link_distance = ld
    data.radio.link_distance2gateway = l2g
    data.radio.gateway2link_distance = g2l

    return data


def is_able_to_get_solution(node: Node, data: dataclass) -> bool:
    """
    Criteria for acceptable placement of stations

    Parameters
    ----------
    node - binary tree node
    data - problem input data

    Returns
    -------
        True or False
    """
    if data.configuration.place_all_station:
        i, _ = np.where(node.left_child.pi == 1)
        if len(i) == len(data.radio.coverage):
            return True
    else:
        if is_able_to_connect_gateways(node.left_child,
                                       data.gateway_coordinate):
            return True
    return False


def check_node(i: int, j: int, node: Node, data: dataclass) -> bool:
    """
    Node check for:
        - connection between left and right gateways;
        - cost constraints;
        - delay constraints.

    Parameters
    ----------
    i - index of placement coordinate
    j - index of placed station
    node - current tree node
    data - input problem data

    Returns
    -------
        True or False
    """
    if data.configuration.place_all_station:
        if check_able_to_connect_station(i, j, node, data):
            return True
    else:
        if (check_able_to_connect_station(i, j, node, data)
                and check_cost(node.left_child, data.restriction.cost_limit)
                and check_delay(node.left_child, data.restriction.delay_limit)):
            return True
    return False


def run(input_dataset: dict) -> None:
    """
    Search for the optimal placement

    Parameters
    ----------
    input_dataset - dict() from JSON-file
    """
    data = prepare(input_dataset)
    assert is_able_to_exist_solution(
        data.radio.link_distance,
        data.radio.link_distance2gateway,
        data.radio.gateway2link_distance,
        data.placement_coordinate,
        data.gateway_coordinate), 'There is not problem for this case'

    n = len(data.placement_coordinate)
    m = len(data.radio.sta)
    print(f'Placement number = {n}')
    print(f'Station number = {m}')
    if data.configuration.place_all_station:
        result = (factorial(n)/(factorial(n-m) * factorial(m))) * factorial(m)
        print(f'Number of feasible placement = {result}')

    """ 
    Starting Searching. Initialize Tree and Schedule
    """
    tree = Tree()
    tree.initiate(data.placement_coordinate,
                  data.gateway_coordinate[1],
                  data.radio.coverage)

    statistics = Schedule(tree.top,
                          data.configuration.method,
                          data.gateway_coordinate)
    statistics.write_station_distance_parameters(
        data.radio.coverage,
        data.radio.link_distance,
        data.radio.link_distance2gateway,
        data.radio.gateway2link_distance)

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
            statistics.add(i, j, parent.left_child)

            """add right node"""
            tree.add_right_node(i, j, parent)
            parent.right_child.noncoverage = parent.noncoverage
            parent.right_child.cost = parent.cost
            parent.right_child.delay = parent.delay
            statistics.add(i, j, parent.right_child)

            if check_node(i, j, parent, data):
                if data.configuration.method == "bab":
                    "Branch and bound method"
                    if check_estimation(i, j, parent, data, statistics):
                        statistics.append_estimates(parent)
                        parent = parent.left_child
                    else:
                        tree.unchecked_node.pop()

                        parent.left_child.close = True
                        statistics.write_close_node(parent.left_child.key)

                        statistics.append_estimates(parent)
                        parent = parent.right_child
                else:
                    "Brute force method"
                    check_noncoverage(parent, data, statistics)
                    statistics.append_estimates(parent)
                    parent = parent.left_child
            else:
                tree.unchecked_node.pop()

                parent.left_child.close = True
                statistics.write_close_node(parent.left_child.key)
                statistics.infeasible_placement_nodes.append(
                    parent.left_child.key)

                statistics.append_estimates(parent)
                parent = parent.right_child
        else:
            parent.close = True
            statistics.write_close_node(parent.key)
            if parent.key not in statistics.record_node:
                statistics.infeasible_placement_nodes.append(parent.key)
            parent = tree.unchecked_node[-1]
            tree.unchecked_node.pop()

    statistics.write_close_node(parent.key)
    if input_dataset["configuration"]["drawing"]:
        plot(tree, statistics)

    statistics.save_json()
    print('Total number of nodes is {}'.format(tree.node_keys[-1]))

