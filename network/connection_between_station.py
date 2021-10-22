"""
CHECKING FEASIBLE PLACEMENT
Base station has communication distance parameter.
We need to check the link between all placed stations from left gateway to
right gateway in tandem network
"""
from typing import Tuple
from dataclasses import dataclass

from binary_search.tree import Node

import numpy as np


def _in_range(place1: float, place2: float,
              communication_distance: float) -> bool:
    """check whether 'first' and 'second' position is in range """
    return abs(place1 - place2) <= communication_distance


def is_able_to_connect_gateways(node: Node, gtw) -> bool:
    """
    Checking link between left gateway and right gateway
    :param node: node of tree
    :param gtw: gateways coordinates
    :return: True if link is able between gateways through placed stations,
    False - otherwise
    """
    return (node.link.left + node.link.right) >= (gtw[1] - gtw[0])


def is_able_to_exist_solution(comm_dist: np.ndarray,
                              comm_dist2gtw: np.array,
                              place: Tuple[float],
                              gtw: Tuple[float]) -> bool:
    """ checking the existence of feasible problem """
    # first_max = max(comm_dist)
    first_max = comm_dist2gtw.max()

    if not (_in_range(gtw[0], place[0], first_max) and
            _in_range(gtw[1], place[-1], first_max)):
        return False

    # second_max = max(comm_dist[i] for i in range(len(comm_dist))
    #                  if i != comm_dist.index(first_max))
    # second_max = np.sort(np.max(comm_dist, axis=0))[-2]
    second_max = comm_dist.max()
    for i in range(len(place) - 1):
        if not _in_range(place[i], place[i + 1], second_max):
            return False
    return True


def is_able_to_connect_to_left_station(p: int, s: int, node: Node,
                                       data: dataclass) -> bool:
    """
    Link condition from the left

    Parameters
    ----------
    p - index of placement
    s - index of station
    node - current node
    data - input data

    Returns
    -------
        True if communication distance (link) is more than the distance
    to the left station, False - otherwise
    """

    node.right_child.link.left = node.link.left
    current_place = data.placement_coordinate[p]

    if 1 in node.pi:  # If any station has been already placed.
        i, j = np.where(node.pi == 1)
        current_link = data.link_distance[s, j[-1]]
        left_place = data.placement_coordinate[i[-1]]
        left_link = data.link_distance[j[-1], s]
        if not _in_range(left_place, current_place, left_link):
            node.close = True
            return False
    else:
        left_place = data.gateway_coordinate[0]
        current_link = data.link_distance2gateway[s]
    if not _in_range(left_place, current_place, current_link):
        node.close = True
        return False
    node.left_child.link.left = node.link.left + (current_place - left_place)

    return True


def is_able_to_connect_to_right_station(p: int, s: int, node: Node,
                                        data: dataclass) -> bool:
    """
    Link condition from the right

    Parameters
    ----------
    p - index of placement
    s - index of station
    node - current node
    data - input data

    Returns
    -------
        True if communication distance (link) is more than the distance
    to the right station, False - otherwise
    """

    node.right_child.link.right = node.link.right

    i, j = np.where(node.pi == 1)
    unplaced_sta_index = [i for i in range(data.link_distance.shape[0])
                          if (i not in j) and (i is not s)]

    current_place = data.placement_coordinate[p]

    vacant_link_distance = data.link_distance[unplaced_sta_index, :]

    if ((current_place == data.placement_coordinate[-1]) or
            (len(vacant_link_distance) is 0)):
        right_place = data.gateway_coordinate[-1]
        current_link = data.link_distance2gateway[s]
    else:
        vld_j, = np.where(
            data.link_distance[:, s] == vacant_link_distance[:, s].max())
        current_link = data.link_distance[s, vld_j[-1]]
        right_place = data.placement_coordinate[p + 1]

        if not _in_range(right_place,
                         current_place,
                         data.link_distance[vld_j[-1], s]):
            node.close = True
            return False

    if not _in_range(right_place, current_place, current_link):
        node.close = True
        return False
    node.left_child.link.right = current_link
    return True


def is_able_to_connect_vacant_station(p: int, s: int, node: Node,
                                      data: dataclass) -> bool:
    """
    Check link station of vacant station and right places

    Parameters
    ----------
    p - index of placement
    s - index of station
    node - current node
    data - input data

    Returns
    -------
        True if link range of vacant station is more than
    distance or False otherwise
    """

    if p == node.pi.shape[0] - 1:
        return True

    _, j = np.where(node.pi == 1)
    unplaced_sta_index = [i for i in range(data.link_distance.shape[0])
                          if (i not in j) and (i is not s)]
    unplaced_stat_link_distance = data.link_distance[unplaced_sta_index, :]

    if len(unplaced_stat_link_distance) == 0:
        return True

    uld_j, = np.where(
        data.link_distance[:, s] == unplaced_stat_link_distance[:, s].max())

    if len(unplaced_stat_link_distance) == 1:
        node.close = True
        if p is data.placement_coordinate.index(data.placement_coordinate[-1]):
            node.close = not _in_range(data.placement_coordinate[p],
                                       data.gateway_coordinate[-1],
                                       data.link_distance2gateway[s])
        else:
            for right_p in (data.placement_coordinate[p + 1:]):
                bool1 = _in_range(data.placement_coordinate[p], right_p,
                                  data.link_distance[uld_j[-1], s])
                bool2 = _in_range(right_p, data.gateway_coordinate[-1],
                                  data.link_distance2gateway[uld_j[-1]])
                node.close = not (bool1 and bool2)
            return not node.close

    if len(unplaced_stat_link_distance) > 1:
        first_max = data.link_distance2gateway[unplaced_sta_index].max()
        second_max = unplaced_stat_link_distance.max()
        for i in range(len(data.placement_coordinate[p + 1:])):
            if i == len(data.placement_coordinate) - 1:
                if _in_range(data.gateway_coordinate[-1],
                             data.placement_coordinate[i], first_max):
                    return True
            else:
                if _in_range(data.placement_coordinate[i + 1],
                             data.placement_coordinate[i], second_max):
                    return True
    return False


def check_able_to_connect_station(i: int, j: int, node: Node,
                                  data: dataclass) -> bool:
    """
    Check link conditions

    Parameters
    ----------
    i - index of placement
    j - index of station
    node - current node
    data - input data

    Returns
    -------
        True if STA can be connected with left and right STAs and False
    otherwise
    """

    if (is_able_to_connect_to_left_station(i, j, node, data) and
            is_able_to_connect_to_right_station(i, j, node, data)
            and is_able_to_connect_vacant_station(i, j, node, data)):
        return True
    return False