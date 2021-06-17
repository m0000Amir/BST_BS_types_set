"""
CALCULATION OF EVALUATIONS
- node noncoverage;
- node cost;
- node delay
"""
from .bst import Node
from typing import Tuple, Any

import numpy as np


def noncov_btwn_sta(place1: float, place2: float,
                    cov1: float, cov2: float) -> float:
    """
    Calculate noncoverage between place1 and place2
    :param place1:
    :param place2:
    :param cov1:
    :param cov2:
    :return: Noncoverage between two placed station
    """
    dist = abs(place2 - place1)
    cov = cov1 + cov2
    return max([dist - cov, 0])


def solve_noncoverage(p: int, s: int, node: Node, gtw: Tuple[float],
                      place: Tuple[Any], cov: Tuple[Any]) -> float:
    """
    Calculate estimates of noncoverage
    :param p: index of placement
    :param s: index of station
    :param node: parent node
    :param gtw: gateways coordinates
    :param place: placement coordinates
    :param cov: stations coverage radius

    :return: Noncoverage
    """
    i, j = np.where(node.pi == 1)

    if len(i) == 0:  # searching is just started
        left_sta_place = gtw[0]
        left_sta_cov = 0
    else:
        left_sta_place = place[i[-1]]
        left_sta_cov = cov[j[-1]]

    # left noncoverage
    left_noncov = node.noncov.left + noncov_btwn_sta(left_sta_place,
                                                     place[p],
                                                     left_sta_cov,
                                                     cov[s])
    # right noncoverage
    unbusy_sta_cov = [cov[i] for i in range(len(cov))
                      if (i not in j) and (i != s)]

    unbusy_place = [place[j] for j in range(len(place))
                    if (j not in i) and (j != p)]

    if len(unbusy_sta_cov) > len(unbusy_place):
        sort_cov = unbusy_sta_cov
        sort_cov.sort()
        unbusy_sta_cov = sort_cov[-1:-(len(unbusy_place) + 1):-1]

    right_noncov = noncov_btwn_sta(place[p],
                                   gtw[-1],
                                   cov[s],
                                   sum(2 * unbusy_sta_cov))
    # node noncoverage
    node.left_child.noncov.left = left_noncov
    node.left_child.noncov.right = max((gtw[-1] - place[p]) - cov[s], 0)
    return left_noncov + right_noncov


def solve_cost(node: Node, cost: float) -> float:
    return node.cost + cost


def solve_delay(node: Node, arrival_rate: float,
                average_packet_size: float, throughput: float) -> float:
    """
    Colving node time delay.

    Let's accept the assumption that any station represent as M/M/1 queue, where
    arrivals are determined by a Poisson process and serivice times have an
    exponentional distribution.

    According to Burke's theorem at the exit from the node we also have a
    Poisson flow with arrival rate that is equal to sum of arrival rates of all
    incoming flows.

    """
    departure_rate = throughput / average_packet_size
    # Amount of all placed station is
    _, j = np.where(node.left_child.pi == 1)
    placed_sta_amount = len(j)
    # By Burke's total arrival rate is
    total_arrival_rate = arrival_rate * placed_sta_amount

    rho = total_arrival_rate / departure_rate
    # rho must be less than 0.9 (rho < 1 theoretically)
    if rho <= 0.9:
        # By Little's law the average time delay at each station is
        mean_system_size = rho / (1 - rho)
        mean_service_time = round(mean_system_size / total_arrival_rate, 5)
        return node.delay + mean_service_time
    else:
        return float('inf')
