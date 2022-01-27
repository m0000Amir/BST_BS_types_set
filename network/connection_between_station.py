"""
Checking the availability of communication between placed stations.

Base station has communication link distance parameter.
It's necessary to check the link between all placed stations from
the left gateway to the right gateway in wireless network.
"""
from typing import Tuple
from dataclasses import dataclass

from binary_search.tree import Node

import numpy as np


def _in_range(place1: float, place2: float,
              communication_distance: float) -> bool:
    """
    Communication distance between Tx and Rx must be no less than the
    distance between them.
    Parameters
    ----------
    place1 - coordinate of Tx
    place2 - coordinate of Rx
    communication_distance - communication link distance

    Returns
    -------
    True if communication distance is more the distance between Tx and Rx

    """
    return abs(place1 - place2) <= communication_distance


def is_able_to_connect_gateways(node: Node, gtw) -> bool:
    """
    Checking link between the left gateway and the right gateway
    Parameters
    ----------
    node - node of binary tree
    gtw - gateway coordinates

    Returns
    -------
    True if the link is able between gateways through placed stations,
    False is otherwise
    """
    return (node.link.left + node.link.right) >= (gtw[1] - gtw[0])


def is_able_to_exist_solution(link_distance: np.ndarray,
                              link_distance2gtw: np.array,
                              gtw2link_distance: np.array,
                              place: Tuple[float],
                              gtw: Tuple[float]) -> bool:
    """
    Checking the existence of feasible placement with a given placement
    coordinates and given set of stations.

    Parameters
    ----------
    link_distance - communication link between stations
    link_distance2gtw - communication links between stations and gateway
    gtw2link_distance - communication links between gateway and stations
    place - placement coordinates
    gtw - coordinates of gateways

    Returns
    -------
    True if feasible placement is exist, False is otherwise
    """
    i = np.argmax(link_distance2gtw)
    first_max = link_distance2gtw[i]

    if not (_in_range(gtw[0], place[0], first_max) and
            _in_range(gtw[0], place[0], gtw2link_distance[i]) and
            _in_range(gtw[1], place[-1], first_max) and
            _in_range(gtw[1], place[-1], gtw2link_distance[i])):
        return False

    _comm_dist = link_distance[np.arange(len(link_distance)) != i]
    second_max = link_distance.max()
    for i in range(len(place) - 1):
        if not _in_range(place[i], place[i + 1], second_max):
            return False
    return True


def is_able_to_connect_to_left_station(p: int,
                                       s: int,
                                       node: Node,
                                       data: dataclass) -> bool:
    """
    Link condition from the left

    Parameters
    ----------
    p - index of placement coordinate
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
        current_link = data.radio.link_distance[s, j[-1]]
        left_place = data.placement_coordinate[i[-1]]
        left_link = data.radio.link_distance[j[-1], s]
        if not _in_range(left_place, current_place, left_link):
            node.close = True
            return False
    else:
        left_place = data.gateway_coordinate[0]
        current_link = data.radio.link_distance2gateway[s]
    if not _in_range(left_place, current_place, current_link):
        node.close = True
        return False
    node.left_child.link.left = node.link.left + (current_place - left_place)

    return True


def is_able_to_connect_to_right_station(p: int,
                                        s: int,
                                        node: Node,
                                        data: dataclass) -> bool:
    """
    Link condition with the right placed station

    Parameters
    ----------
    p - index of placement coordinate
    s - index of station
    node - current node
    data - input data

    Returns
    -------
    True if communication link distance is more than the distance
    to the right station, False is otherwise
    """
    node.right_child.link.right = node.link.right

    i, j = np.where(node.pi == 1)
    unplaced_sta_index = [i for i in range(data.radio.link_distance.shape[0])
                          if (i not in j) and (i is not s)]

    current_place = data.placement_coordinate[p]

    vacant_link_distance = data.radio.link_distance[unplaced_sta_index, :]

    if ((current_place == data.placement_coordinate[-1]) or
            (len(vacant_link_distance) == 0)):
        right_place = data.gateway_coordinate[-1]
        current_link = data.radio.link_distance2gateway[s]
    else:
        vld_j, = np.where(
            data.radio.link_distance[:, s] == vacant_link_distance[:, s].max())
        current_link = data.radio.link_distance[s, vld_j[-1]]
        right_place = data.placement_coordinate[p + 1]

        if not _in_range(right_place,
                         current_place,
                         data.radio.link_distance[vld_j[-1], s]):
            node.close = True
            return False

    if not _in_range(right_place, current_place, current_link):
        node.close = True
        return False
    node.left_child.link.right = current_link
    return True


def is_able_to_connect_vacant_station(p: int,
                                      s: int,
                                      node: Node,
                                      data: dataclass) -> bool:
    """
    Check the existence of the connection with the station placed on the
    right vacant  coordinate.

    Parameters
    ----------
    p - index of placement
    s - index of station
    node - current node
    data - input data

    Returns
    -------
    True if the link distance of vacant station is more than
    distance to the right vacant placement coordinate, False is otherwise.
    """

    if p == node.pi.shape[0] - 1:
        return True

    _, j = np.where(node.pi == 1)
    unplaced_sta_index = [i for i in range(data.radio.link_distance.shape[0])
                          if (i not in j) and (i is not s)]
    unplaced_sta_l_d = data.radio.link_distance[unplaced_sta_index, :]

    if len(unplaced_sta_l_d) == 0:
        return True

    uld_j, = np.where(
        data.radio.link_distance[:, s] == unplaced_sta_l_d[:, s].max())

    if len(unplaced_sta_l_d) == 1:
        node.close = True
        if p is data.placement_coordinate.index(data.placement_coordinate[-1]):
            node.close = not _in_range(data.placement_coordinate[p],
                                       data.gateway_coordinate[-1],
                                       data.link_distance2gateway[s])
        else:
            for right_p in (data.placement_coordinate[p + 1:]):
                bool1 = _in_range(data.placement_coordinate[p], right_p,
                                  data.radio.link_distance[uld_j[-1], s])
                bool2 = _in_range(right_p, data.gateway_coordinate[-1],
                                  data.radio.link_distance2gateway[uld_j[-1]])
                node.close = not (bool1 and bool2)
            return not node.close

    if len(unplaced_sta_l_d) > 1:
        first_max = data.radio.link_distance2gateway[unplaced_sta_index].max()
        second_max = unplaced_sta_l_d.max()
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


def check_able_to_connect_station(i: int,
                                  j: int,
                                  node: Node,
                                  data: dataclass) -> bool:
    """
    Check link conditions

    Parameters
    ----------
    i - index of placement coordinate
    j - index of station
    node - current node of binary tree
    data - input data

    Returns
    -------
    True if station can be connected with the left and the right stations,
    False is otherwise.
    """

    if (is_able_to_connect_to_left_station(i, j, node, data) and
            is_able_to_connect_to_right_station(i, j, node, data)
            and is_able_to_connect_vacant_station(i, j, node, data)):
        return True
    return False
