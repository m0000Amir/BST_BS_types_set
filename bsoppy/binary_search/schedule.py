"""
Solution schedule for Binary Search Tree
"""
import json

from bsoppy.binary_search.tree import Node

from termcolor import colored
import numpy as np


class Schedule:
    def __init__(self, top: Node, method: str, gtw_coordinate) -> None:
        self.method = method
        self.placement_count = top.pi.shape[0]
        self.station_count = top.pi.shape[1]
        self.coverage = None
        self.link_distance = None
        self.link_distance2gtw = None
        self.gtw2link_distance = None
        self.place = list()
        self.station = list()
        self.pi = list()
        self.estimate = {top.key: top.noncoverage.estimate}
        self.noncoverage = list()
        self.cost = list()
        self.delay = list()
        self.step = list()
        """ Obtained Records"""
        self.records = list()
        self.record_noncoverage = [gtw_coordinate[1]-gtw_coordinate[0]]
        self.record_pi = list()
        self.record_cost = list()
        self.record_delay = list()
        self.record_node = list()
        self._record_type = None
        self.print_record = list()
        self.infeasible_placement_nodes = list()
        self.close_nodes = list()
        self.placed_sta = list()
        self.add(float('inf'), float('inf'), top)

    def __str__(self):
        if self._record_type == "Optimal":
            color = "magenta"
        else:
            color = "cyan"
        return (colored(f"{self._record_type} = {self.record_noncoverage[-1]}, "
                        f"Cost = {self.record_cost[-1]},  "
                        f"Delay = {self.record_delay[-1]:.5f},  "
                        f"Node = {self.record_node[-1]}",
                        color, attrs=['bold', 'blink']) +
                "\n" +
                colored(self.placed_sta[-1], 'magenta',
                        'on_green', attrs=['bold']))

    def append_record(self, node: Node, optimal=None, feasible=None) -> None:
        """
        Adding a new record to the schedule

        Parameters
        ----------
        node - binary tree node
        optimal - optimal record
        feasible - feasible record

        Returns
        -------
            None
        """
        if optimal is not None:
            self.record_noncoverage.append(optimal)
            self._record_type = "Optimal"

        elif feasible is not None:
            self.record_noncoverage.append(feasible)
            self._record_type = '\tFeasible'
        self.record_cost.append(node.left_child.cost)
        self.record_delay.append(node.left_child.delay)
        self.record_node.append(node.left_child.key)

        i, j = np.where(node.left_child.pi == 1)
        placed_sta = ['-'] * self.placement_count
        for k in range(len(i)):
            placed_sta[i[k]] = 'S' + str(j[k] + 1)
        self.placed_sta.append(placed_sta)

        self.records.append(
            {"type": self._record_type,
             "noncoverage": self.noncoverage[-1],
             "cost": self.cost[-1],
             "delay": self.delay[-1],
             "node": self.record_node[-1],
             "placed_sta": placed_sta}
        )

    def add(self, p, s, node) -> None:
        """
        Adding of New Row on Schedule

        Parameters
        ----------
        p - index of placement coordinate
        s - index of station
        node - binary tree node
        """
        self.place.append(p)
        self.station.append(s)
        self.pi.append(node.pi[p, s] if p != float('inf') else float('inf'))
        self.noncoverage.append(node.noncoverage.left + node.noncoverage.right)
        self.cost.append(node.cost)
        self.delay.append(node.delay)
        self.step.append(node.key)

    def write_close_node(self, key: int) -> None:
        """
        Writing close nodes of binary tree on schedule

        Parameters
        ----------
        key - key of binary tree node

        """
        self.close_nodes.append(key)

    def append_estimates(self, node: Node) -> None:
        """
        Appending noncoverage estimate on the current node

        Parameters
        ----------
        node - binary tree node
        """
        self.estimate.update(
            {node.left_child.key: node.left_child.noncoverage.estimate})
        self.estimate.update(
            {node.right_child.key: node.right_child.noncoverage.estimate})

    def write_station_distance_parameters(self,
                                          cov: np.ndarray,
                                          ld: np.ndarray,
                                          l2g: np.ndarray,
                                          g2l: np.ndarray) -> None:
        """ Writing radio communication parameters of station on schedule"""
        self.coverage = cov
        self.link_distance = ld
        self.link_distance2gtw = l2g
        self.gtw2link_distance = g2l

    def save_json(self) -> None:
        """ Obtained solution """
        solution = {"coverage": self.coverage.tolist(),
                    "link": {
                        "link_distance": self.link_distance.tolist(),
                        "link_distance2gtw": self.link_distance2gtw.tolist(),
                        "gtw2link_distance": self.gtw2link_distance.tolist()
                    },
                    "records": self.records}

        json_object = json.dumps(solution)
        obj = open('./solution.json', 'w')
        obj.write(json_object)
        obj.close()
