"""
Branch and Bound

If node noncoverage estimate is not less or equal than a calculated record then
node is closed. Also cost and delay is checked.

"""
from typing import Tuple, Any


from bab.bst import Node
from bab.feasible_placement import is_able_link_btwn_gtw
# from bab.evaluation import mean_service_time
from bab.schedule import Schedule
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
                   cov: Tuple[Any], cost: Tuple[Any],
                   cost_limit: int, delay_limit: int,
                   deviation: float, eng) -> bool:
    """
    Getting new noncoverage record
    :param node: node of binary tree
    :param statistics: record schedule
    :param place: coordinates of placements
    :param gtw: gateways coordinates
    :param deviation: deviation from record
    :param delay_limit: problem delay limit
    :param cost_limit: problem cost limit
    :return: True if noncoverage_estiate is not more than obtained record,
    False - otherwise
    """
    [node.left_child.noncov.estimate, move_bool] = get_noncoverage(p, s, node,
                                                                   gtw, place,
                                                                   cov, cost,
                                                                   cost_limit,
                                                                   eng)
    # if move_bool is False:
    #     return False

    statistics.add(p, s, node.left_child)

    if (node.left_child.noncov.estimate < (statistics.record[-1]) and
            check_cost(node.left_child, cost_limit) and
            check_delay(node.left_child, delay_limit)):
        if is_able_link_btwn_gtw(node.left_child, gtw):
            node_noncov = (node.left_child.noncov.left +
                           node.left_child.noncov.right)
            if ((node_noncov < statistics.record[-1]) and
                    node.left_child.cost <= statistics.cost[-1] and
                    node.left_child.delay <= statistics.delay[-1]):
                statistics.record.append(node_noncov)

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


def check_estimate_old_func(node: Node, statistics: Schedule,
                            place: Tuple[float], gtw: Tuple[float],
                            cost_limit: int, delay_limit: int,
                            deviation: float) -> bool:
    """
    Getting new noncoverage record
    :param node: node of binary tree
    :param statistics: record schedule
    :param place: coordinates of placements
    :param gtw: gateways coordinates
    :param deviation: deviation from record
    :param delay_limit: problem delay limit
    :param cost_limit: problem cost limit
    :return: True if noncoverage_estiate is not more than obtained record,
    False - otherwise
    """
    if (node.noncov.estimate <= (statistics.record[-1]) and
            check_cost(node, cost_limit) and check_delay(node, delay_limit)):
        if is_able_link_btwn_gtw(node, gtw):
            node_noncov = node.noncov.left + node.noncov.right
            if ((node_noncov < statistics.record[-1]) and
                    node.cost <= statistics.cost[-1] and
                    node.delay <= statistics.delay[-1]):
                statistics.record.append(node_noncov)

                print(statistics)
                i, j = np.where(node.pi == 1)
                placed_sta = ['-'] * len(place)

                for k in range(len(i)):
                    placed_sta[i[k]] = 'S' + str(j[k] + 1)
                print(colored(placed_sta, 'magenta', 'on_green',
                              attrs=['bold']))
        return True
    else:
        return False
