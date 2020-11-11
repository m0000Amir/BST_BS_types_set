"""
Solution schedule for Binary search tree
Record is printed at each node if noncoverage estimate is no more than last
record.
"""


from termcolor import colored


class Schedule:
    """
    Solution record
    """
    def __init__(self):
        self.place = list()
        self.station = list()
        self.pi = list()
        self.estimate = list()
        self.noncoverage = list()
        self.cost = list()
        self.delay = list()
        self.step = list()
        self.record = list()
        self.print_record = list()

    def __str__(self):
        return colored("Record = {},  Cost = {},  Delay =  {},  node = {}".format(
            self.noncoverage[-1], self.cost[-1], self.delay[-1], self.step[-1]),
            'magenta', attrs=['bold', 'blink'])

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
        self.estimate.append(node.noncov.estimate)
        self.noncoverage.append(node.noncov.left + node.noncov.right)
        self.cost.append(node.cost)
        self.delay.append(node.delay)
        self.step.append(node.key)

