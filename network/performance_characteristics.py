"""
CALCULATION OF PERFORMANCE CHARACTERISTICS
    - noncoverage;
    - cost;
    - end-to-end delay

Note:
    "Noncoverage" is equal to a difference between the length of a given line
    section and the total coverage of placed stations.
"""
from binary_search.tree import Node
from typing import Tuple, Any

import numpy as np


def noncoverage_between_station(place1: float, place2: float,
                                cov1: float, cov2: float) -> float:
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
                      gtw: Tuple[float],
                      place: Tuple[Any],
                      cov: np.ndarray) -> Tuple[float, float]:
    """
    Calculate the total noncoverage of all placed station in this node

    Parameters
    ----------
    p - index of placement
    s - index of station
    node - parent node
    gtw - gateways coordinates
    place - placement coordinates
    cov - stations coverage

    Returns
    -------
        The total noncoverage in node

    """
    i, j = np.where(node.pi == 1)

    if len(i) == 0:  # searching is just started
        left_station_placement_point = gtw[0]
        left_station_coverage = 0
    else:
        left_station_placement_point = place[i[-1]]
        left_station_coverage = cov[j[-1]]

    # left noncoverage
    left_noncoverage = (node.noncoverage.left +
                        noncoverage_between_station(
                            left_station_placement_point,
                            place[p],
                            left_station_coverage,
                            cov[s]))

    # right noncoverage
    right_noncoverage = max((gtw[-1] - place[p]) - cov[s], 0)

    # vacant_stations_coverage = [cov[i] for i in range(len(cov))
    #                             if (i not in j) and (i != s)]
    #
    # vacant_placement_point = [place[j] for j in range(len(place))
    #                           if (j not in i) and (j != p)]
    #
    # if len(vacant_stations_coverage) > len(vacant_placement_point):
    #     _sort_cov = vacant_stations_coverage
    #     _sort_cov.sort()
    #     vacant_stations_coverage = _sort_cov[
    #                                -1:-(len(vacant_placement_point) + 1):-1]
    #
    # right_noncoverage = noncoverage_between_station(
    #     place[p],
    #     gtw[-1],
    #     cov[s],
    #     sum(2 * vacant_stations_coverage))

    # node noncoverage
    # node.left_child.noncoverage.left = left_noncoverage
    # node.left_child.noncoverage.right = max((gtw[-1] - place[p]) - cov[s], 0)
    return left_noncoverage, right_noncoverage

def solve_cost(node: Node, cost: float) -> float:
    """
    Calculate cost of all placed station in this node

    Parameters
    ----------
    node - node of binary search tree
    cost - cost of placed station

    Returns
    -------
        The total cost in node
    """
    return node.cost + cost


def solve_delay(node: Node, arrival_rate: float,
                average_packet_size: float, throughput: float) -> float:
    """
    Solving end-end delay using stochastic queueing model.

    Let's accept the assumption that any station represent as M/M/1 queue, where
    arrivals are determined by a Poisson process and service times have an
    exponential distribution.

    According to Burke's theorem at the exit from the node we also have a
    Poisson flow with arrival rate that is equal to sum of arrival rates of all
    incoming flows.

    Parameters
    ----------
    node - parent node
    arrival_rate - rate of incoming traffic
    average_packet_size - packet size of traffic
    throughput - throughput of node

    Returns
    -------
        End-to-end delay
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
