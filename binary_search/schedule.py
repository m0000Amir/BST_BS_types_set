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
    def __init__(self, top: Node) -> None:
        self.place = list()
        self.station = list()
        self.pi = list()
        self.estimate = list()
        self.noncoverage = list()
        self.cost = list()
        self.delay = list()
        self.step = list()
        self.record = [{'optimal': None, 'subsequence': list()}]
        self._record_type = None
        self.print_record = list()
        self.add(float('inf'), float('inf'), top)

    def __str__(self):
        if self._record_type == "Optimal":
            color = "magenta"
        else:
            color = "cyan"

        return colored("{} = {},  Cost = {},  Delay =  {},  node = {}".format(
            self._record_type, self.noncoverage[-1], self.cost[-1],
            self.delay[-1], self.step[-1]),
            color, attrs=['bold', 'blink'])

    def append_record(self, optimal=None, feasible=None) -> None:
        if optimal is not None:
            self.record.append({'optimal': None, 'subsequence': list()})
            self.record[-1]['optimal'] = optimal
            self._record_type = "Optimal"
        elif feasible is not None:
            # self.record.append({'optimal': None, 'subsequence': list()})
            self.record[-1]['subsequence'].append(feasible)
            self._record_type = '\tFeasible'

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
        self.estimate.append(node.noncoverage.estimate)
        self.noncoverage.append(node.noncoverage.left + node.noncoverage.right)
        self.cost.append(node.cost)
        self.delay.append(node.delay)
        self.step.append(node.key)

