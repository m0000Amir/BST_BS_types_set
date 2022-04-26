"""
CALCULATION OF PERFORMANCE CHARACTERISTICS
    - noncoverage;
    - cost;
    - end-to-end delay

Note:
    "Noncoverage" is equal to a difference between the length of a given line
    section and the total coverage of placed stations.
"""
from typing import Tuple
from dataclasses import dataclass

from bsoppy.binary_search.tree import Node

import numpy as np


def noncoverage_between_station(place1: float,
                                place2: float,
                                cov1: float,
                                cov2: float) -> float:
    """
    Calculate noncoverage between placed station 1 and placed station 2

    Parameters
    ----------
    place1 - placement point of station 1
    place2 - placement point of station 1
    cov1 - coverage of station 1
    cov2 - coverage of station 2

    Returns
    -------
    The total noncoverage between station 1 and station 2
    """
    dist = abs(place2 - place1)
    cov = cov1 + cov2
    return max([dist - cov, 0])


def solve_noncoverage(p: int,
                      s: int,
                      node: Node,
                      data: dataclass) -> Tuple[float, float]:
    """
    Calculate the total noncoverage of all placed station in this node

    Parameters
    ----------
    p - index of placement
    s - index of station
    node - parent node
    data - input data

    Returns
    -------
    The total noncoverage in node
    """
    i, j = np.where(node.pi == 1)

    if len(i) == 0:  # searching is just started
        left_station_placement_point = data.gateway_coordinate[0]
        left_station_coverage = 0
    else:
        left_station_placement_point = data.placement_coordinate[i[-1]]
        left_station_coverage = data.radio.coverage[j[-1]]

    # left noncoverage
    left_noncoverage = (node.noncoverage.left +
                        noncoverage_between_station(
                            left_station_placement_point,
                            data.placement_coordinate[p],
                            left_station_coverage,
                            data.radio.coverage[s]))

    # right noncoverage
    distance_to_right_gateway = (data.gateway_coordinate[-1] -
                                 data.placement_coordinate[p])
    right_noncoverage = max(
        distance_to_right_gateway - data.radio.coverage[s], 0
    )

    return left_noncoverage, right_noncoverage


def solve_cost(s: int, node: Node, data: dataclass) -> float:
    """
    Calculate cost of all placed station in this node

    Parameters
    ----------
    s - index of station
    node - node of binary search tree
    data - input_data

    Returns
    -------
    The total cost in node
    """
    return node.cost + data.cost[s]


def solve_delay(s, node: Node, data: dataclass) -> float:
    """
    Solving end-to-end delay using stochastic queueing model.

    Let's accept the assumption that any station represent as M/M/1 queue,
    where arrivals are determined by a Poisson process and service times
    have an exponential distribution.

    According to Burke's theorem at the exit from the node we also have a
    Poisson flow with arrival rate that is equal to sum of arrival rates
    of all incoming flows.

    Parameters
    ----------
    s - index of station
    node - parent node
    data - input data

    Returns
    -------
    End-to-end delay
    """

    departure_rate = 0.5*data.throughput[s] / data.arrival.packet_size
    # Amount of all placed station is
    _, j = np.where(node.left_child.pi == 1)
    placed_sta_amount = len(j)
    # By Burke's total arrival rate is
    total_arrival_rate = data.arrival.rate * placed_sta_amount

    rho = total_arrival_rate / departure_rate
    # rho must be less than 0.9 (rho < 1 theoretically)
    if rho <= 0.9:
        # By Little's law the average time delay at each station is
        mean_system_size = rho / (1 - rho)
        mean_service_time = round(mean_system_size / total_arrival_rate, 5)
        return node.delay + mean_service_time
    else:
        """Stationarity condition"""
        return float('inf')


def check_cost(node: Node, cost_limit: int) -> bool:
    """
    Checking cost estimate for getting new noncoverage record
    Parameters
    ----------
    node - left child node of binary search tree
    cost_limit - cost limit of the problem

    Returns
    -------
    True if the cost of the placed station is less than the cost limit,
    False is otherwise
    """
    return node.cost <= cost_limit


def check_delay(node: Node, delay_limit: int) -> bool:
    """
    Checking delay estimate for getting new noncoverage record
    Parameters
    ----------
    node - left child node of binary search tree
    delay_limit - delay limit of the problem

    Returns
    -------
    True if the end-to-end delay of the placed station is less than the delay
    limit, False is otherwise
    """
    if node.delay == float('inf'):
        # It means that service utilization is more than 0.9 (rho > 1)
        return False
    return node.delay <= delay_limit
