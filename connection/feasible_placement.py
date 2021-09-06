"""
CHECKING FEASIBLE PLACEMENT
Base station has communication distance parameter.
We need to check the link between all placed stations from left gateway to
right gateway in tandem network
"""
from typing import Tuple, Any

from bab.bst import Node

import numpy as np


def _in_range(place1: float, place2: float,
              communication_distance: float) -> bool:
    """check whether 'first' and 'second' position is in range """
    return abs(place1 - place2) <= communication_distance


def is_able_link_btwn_gtw(node: Node, gtw) -> bool:
    """
    Checking link between left gateway and right gateway
    :param node: node of tree
    :param gtw: gateways coordinates
    :return: True if link is able between gateways through placed stations,
    False - otherwise
    """
    return (node.link.left + node.link.right) >= (gtw[1] - gtw[0])


def is_able_to_exist_solution(comm_dist: np.ndarray, comm_dist2gtw: np.array,
                              place: Tuple[float],
                              gtw: Tuple[float]) -> bool:

    """ checking the existence of feasible solution """
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


def is_able_link_left(p: int, s: int, node: Node, place: Tuple[float],
                      comm_dist: np.ndarray, comm_dist2gtw: np.ndarray,
                      gtw: Tuple[float]) -> bool:
    """
    Link condition from the left
    :param p: index of placement
    :param s: index of station
    :param node: current node
    :param place: placement coordinates
    :param comm_dist: communication distance (link) of stations
    :param comm_dist2gtw: communication distance (link) between stations and
    gateways
    :param gtw: gateways coordinates
    :return: -True if communication distance (link) is more than the distance
    to the left station, False - otherwise
    """
    node.right_child.link.left = node.link.left
    current_place = place[p]
    # current_link = comm_dist[s]

    if 1 in node.pi:  # If any station has been already placed.
        i, j = np.where(node.pi == 1)
        current_link = comm_dist[s, j[-1]]
        left_place = place[i[-1]]
        left_link = comm_dist[j[-1], s]
        if not _in_range(left_place, current_place, left_link):
            node.close = True
            return False
    else:
        left_place = gtw[0]
        current_link = comm_dist2gtw[s]
    if not _in_range(left_place, current_place, current_link):
        node.close = True
        return False
    node.left_child.link.left = node.link.left + (current_place - left_place)

    return True


def is_able_link_right(p: int, s: int, node: Node, place: Tuple[float],
                       comm_dist: np.ndarray, comm_dist2gtw: np.ndarray,
                       gtw: Tuple[float]) -> bool:
    """
    Link condition from the right
    :param p: index of placement
    :param s: index of station
    :param node: current node
    :param place: placement coordinates
    :param comm_dist: communication distance (link) of stations
    :param comm_dist2gtw: communication distance (link) between stations and
    gateways
    :param gtw: gateways coordinates
    :return: -True if communication distance (link) is more than the distance
    to the right station, False - otherwise
    """
    node.right_child.link.right = node.link.right

    i, j = np.where(node.pi == 1)
    unplaced_sta_index = [i for i in range(comm_dist.shape[0]) if (i not in j)
                          and (i is not s)]
    # unplaced_comm_link = comm_dist[unplaced_sta_index, :]
    # ucd_j, = np.where(comm_dist[:, s] == unplaced_comm_link[:, s].max())
    current_place = place[p]
    # current_link = comm_dist[s, ucd_j[-1]]
    # placed_sta_comm_link = [comm_dist[i] for i in j] + [current_link]
    unplaced_comm_link = comm_dist[unplaced_sta_index, :]


    if ((current_place == place[-1]) or
            (len(unplaced_comm_link) is 0)):
        right_place = gtw[-1]
        current_link = comm_dist2gtw[s]
    else:
        ucd_j, = np.where(comm_dist[:, s] == unplaced_comm_link[:, s].max())
        current_link = comm_dist[s, ucd_j[-1]]
        right_place = place[p + 1]
        # unplaced_sta_link = [comm_dist[i]
        #                      for i in range(len(comm_dist))
        #                      if (i not in j) and i != s]
        # max_link = max(unplaced_sta_link)
        if not _in_range(right_place, current_place, comm_dist[ucd_j[-1], s]):
            node.close = True
            return False

    if not _in_range(right_place, current_place, current_link):
        node.close = True
        return False
    node.left_child.link.right = current_link
    return True


def is_able_link_unbusy_sta(p: int, s: int, node: Node, place: Tuple[float],
                            comm_dist: np.ndarray, comm_dist2gtw: np.ndarray,
                            gtw: Tuple[float]) -> bool:
    """
    check unbusy_sta_link station and right places
    :param p: index of placement
    :param s: index of station
    :param node: current node
    :param place: placement coordinates
    :param comm_dist: communication distance (link) of stations
    :param comm_dist2gtw: communication distance (link) between stations and
    gateways
    :param gtw: gateways coordinates
    :return: True if link range of unbusy_sta_link station is more than
    distance or False otherwise
    """
    if p == node.pi.shape[0] - 1:
        return True

    _, j = np.where(node.pi == 1)
    unplaced_sta_index = [i for i in range(comm_dist.shape[0]) if (i not in j)
                          and (i is not s)]
    unplaced_comm_link = comm_dist[unplaced_sta_index, :]
    # ucd_j, = np.where(comm_dist[:, s] == unplaced_comm_link[:, s].max())

    if len(unplaced_comm_link) == 0:
        return True

    ucd_j, = np.where(comm_dist[:, s] == unplaced_comm_link[:, s].max())

    if len(unplaced_comm_link) == 1:
        node.close = True
        if p is place.index(place[-1]):
            node.close = not _in_range(place[p], gtw[-1], comm_dist2gtw[s])
        else:
            for right_p in (place[p + 1:]):
                bool1 = _in_range(place[p], right_p, comm_dist[ucd_j[-1], s])
                bool2 = _in_range(right_p, gtw[-1], comm_dist2gtw[ucd_j[-1]])
                node.close = not (bool1 and bool2)
            return not node.close

    if len(unplaced_comm_link) > 1:
        first_max = comm_dist2gtw[unplaced_sta_index].max()
        second_max = unplaced_comm_link.max()
        for i in range(len(place[p + 1:])):
            if i == len(place) - 1:
                if _in_range(gtw[-1], place[i], first_max):
                    # node.close is False
                    return True
            else:
                if _in_range(place[i + 1], place[i], second_max):
                    # node.close is False
                    return True
    return False


def check_link(i: int, j: int, node: Node, place, comm_dist: np.ndarray,
               comm_dist2gtw: np.ndarray, gtw: Tuple[float]) -> bool:
    """
    Check link conditions
    :param i: index of placement
    :param j: index of station
    :param node: current node
    :param place: placement coordinates
    :param comm_dist: communication distance (link) of stations
    :param comm_dist2gtw: communication distance (link) between stations and
    gateways
    :param gtw: gateways coordinate
    :return: True if STA can be connected with left and right STAs and False
    otherwise
    """
    if (is_able_link_left(i, j, node, place, comm_dist, comm_dist2gtw, gtw) and
            is_able_link_right(i, j, node, place, comm_dist, comm_dist2gtw, gtw)
            and is_able_link_unbusy_sta(i, j, node, place, comm_dist,
                                        comm_dist2gtw, gtw)):
        return True
    return False
