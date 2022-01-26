from binary_search.tree import Node

from binary_search.schedule import Schedule
from network.connection_between_station import is_able_to_connect_gateways


from dataclasses import dataclass


def check_noncoverage(p: int,
                      s: int,
                      node: Node,
                      data: dataclass,
                      statistics: Schedule) -> None:
    """
    Check noncoverage. If noncoverage is less to Record than noncoverage
    becomes new record.

    Parameters
    ----------
    p - index of placement
    s - index of station
    node - node of binary tree
    data - input data
    statistics - record schedule

    Returns
    -------
        True if noncoverage_estimate is not more than obtained record,
        False - otherwise
    """
    from binary_search.get import is_able_to_get_solution

    # if is_able_to_connect_gateways(node.left_child,
    #                                data.gateway_coordinate):

    if is_able_to_get_solution(node, data):
        node_noncoverage = (node.left_child.noncoverage.left +
                            node.left_child.noncoverage.right)


        # if node_noncoverage < statistics.record[-1]['optimal']:
        #     statistics.append_record(optimal=node_noncoverage)
        #     statistics.add(p, s, node.left_child)
        #     print(statistics)
        #     print_placed_station(node, data)


        statistics.append_record(node, optimal=node_noncoverage)
        # statistics.add(p, s, node.left_child)
        print(statistics)
        print_placed_station(node, data)

        # statistics.add(p, s, node.left_child)

