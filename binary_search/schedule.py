"""
Solution schedule for Binary search tree
Record is printed at each node if noncoverage estimate is no more than last
record.
"""

from termcolor import colored
from binary_search.tree import Node


class Schedule:
    """
    Solution record
    """
    def __init__(self, top: Node, method: str) -> None:
        self.method = method
        self.place = list()
        self.station = list()
        self.pi = list()
        self.estimate = {top.key: top.noncoverage.estimate}
        self.noncoverage = list()
        self.cost = list()
        self.delay = list()
        self.step = list()
        """ Obtained Records"""
        self.record = [{'optimal': None, 'subsequence': list()}]
        self.record_noncoverage = list()
        self.record_cost = list()
        self.record_delay = list()
        self.record_node = list()
        self._record_type = None
        self.print_record = list()
        self.infeasible_placement_nodes = list()
        self.close_nodes = list()

        self.add(float('inf'), float('inf'), top)

    def __str__(self):
        if self._record_type == "Optimal":
            color = "magenta"
            key = "optimal"
        else:
            color = "cyan"
            key = "subsequence"

        return colored("{} = {},  Cost = {},  Delay =  {:.5f},  node = {} /"
                       "".format(
            self._record_type,
            self.record_noncoverage[-1],
            self.record_cost[-1],
            self.record_delay[-1],
            self.record_node[-1]),
            color, attrs=['bold', 'blink'])

    def append_record(self, node: Node, optimal=None, feasible=None) -> None:
        if optimal is not None:
            self.record.append({'optimal': None,
                                'subsequence': list()})
            self.record[-1]['optimal'] = optimal
            self.record_noncoverage.append(optimal)
            self.record_cost.append(node.left_child.cost)
            self.record_delay.append(node.left_child.delay)
            self.record_node.append(node.left_child.key)
            self._record_type = "Optimal"

        elif feasible is not None:
            self.record[-1]['subsequence'].append(feasible)
            self._record_type = '\tFeasible'
            self.record_noncoverage.append(feasible)
            self.record_cost.append(node.left_child.cost)
            self.record_delay.append(node.left_child.delay)
            self.record_node.append(node.left_child.key)

    def add(self, p, s, node):
        """

        :param p: index of placement
        :param s: index of station
        :param node: tree node
        :return: new row of Solution table
        """
        self.place.append(p)
        self.station.append(s)
        self.pi.append(node.pi[p, s] if p != float('inf') else float('inf'))
        self.noncoverage.append(node.noncoverage.left + node.noncoverage.right)
        self.cost.append(node.cost)
        self.delay.append(node.delay)
        self.step.append(node.key)

    def write_close_node(self, key: int):
        self.close_nodes.append(key)

    def append_estimates(self, node: Node) -> None:
        self.estimate.update(
            {node.left_child.key: node.left_child.noncoverage.estimate})
        self.estimate.update(
            {node.right_child.key: node.right_child.noncoverage.estimate})
