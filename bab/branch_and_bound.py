"""
Branch and Bound

If node noncoverage estimate is not less or equal than a calculated record then
node is closed. Also cost and delay is checked.

"""
from typing import Tuple, Any

from binary_search.tree import Node
from network.connection_between_station import is_able_to_connect_gateways
# from bab.evaluation import mean_service_time
from binary_search.schedule import Schedule
from estimation.noncoverage import get_noncoverage

import numpy as np
from termcolor import colored


def check_cost(node: Node, cost_limit: int) -> bool:
    """
    Checking cost estimate for getting new noncoverage record
    :param node: left node of binary search tree
    :param cost_limit: cost limit of the problem
    :return: True if total cost of tree node is less than problem limit,
    False - otherwise
    """
    return node.cost <= cost_limit


def check_delay(node: Node, delay_limit: int) -> bool:
    """
    Checking delay estimate for getting new noncoverage record
    :param node: left node of binary search tree
    :param delay_limit: cost limit of the problem
    :return: True if total cost of tree node is less than problem limit,
    False - otherwise
    """
    if node.delay == float('inf'):
        # It means that service utilization is more than 0.9 (rho > 1)
        return False
    return node.delay <= delay_limit


def check_estimate(p: int, s: int, node: Node, statistics: Schedule,
                   place: Tuple[float], gtw: Tuple[float],
                   cov: np.ndarray, cost: Tuple[Any],
                   cost_limit: int, delay_limit: int,
                   deviation: float, eng) -> bool:
    """

    Parameters
    ----------
    p - index of placement
    s - index of station
    node - node of binary tree
    statistics - record schedule
    place - coordinates of placements
    gtw - gateways coordinates
    cov - stations coverage
    cost - stations cost
    cost_limit - deviation from record
    delay_limit - problem delay limit
    deviation - problem cost limit
    eng - MatLab engine

    Returns
    -------
        True if noncoverage_estiate is not more than obtained record,
        False - otherwise
    """

    node.left_child.noncov.estimate = get_noncoverage(p, s, node,
                                                      gtw, place,
                                                      cov, cost,
                                                      cost_limit,
                                                      eng)

    statistics.add(p, s, node.left_child)
    # if (node.left_child.noncov.estimate <= statistics.record[-1] and
    #         check_cost(node.left_child, cost_limit) and
    #         check_delay(node.left_child, delay_limit)):
    #     TODO: make this condition! ALARM (deviation in the commented code)
    if (node.left_child.noncov.estimate <= ((statistics.record[-1]['optimal'])
                                            + deviation) and
            check_cost(node.left_child, cost_limit) and
            check_delay(node.left_child, delay_limit)):
        if is_able_to_connect_gateways(node.left_child, gtw):
            node_noncov = (node.left_child.noncov.left +
                           node.left_child.noncov.right)

            # write_estimate(node_noncov, statistics, deviation)

            if node_noncov < statistics.record[-1]['optimal']:
                statistics.append_record(optimal=node_noncov)
            elif node_noncov <= statistics.record[-1]['optimal'] + deviation:
                statistics.append_record(feasible=node_noncov)
            else:
                return False

            print(statistics)
            i, j = np.where(node.left_child.pi == 1)
            placed_sta = ['-'] * len(place)

            for k in range(len(i)):
                placed_sta[i[k]] = 'S' + str(j[k] + 1)
            print(colored(placed_sta, 'magenta', 'on_green',
                          attrs=['bold']))
        return True
    else:
        return False
