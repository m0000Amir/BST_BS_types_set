from dataclasses import dataclass

from binary_search.tree import Node
from binary_search.schedule import Schedule


def check_noncoverage(node: Node,
                      data: dataclass,
                      statistics: Schedule) -> None:
    """
    Check noncoverage. If noncoverage is less to Record than noncoverage
    becomes new record.

    Parameters
    ----------
    node - node of binary tree
    data - input data
    statistics - record schedule

    Returns
    -------
        True if noncoverage_estimate is not more than obtained record,
        False - otherwise
    """
    from binary_search.get import is_able_to_get_solution

    if is_able_to_get_solution(node, data):
        node_noncoverage = (node.left_child.noncoverage.left +
                            node.left_child.noncoverage.right)

        statistics.append_record(node, optimal=node_noncoverage)
        print(statistics)
