""" Binary Search Tree for Optimal Placement problem of stations"""
from typing import List, Tuple

import networkx as nx
import numpy as np


class ParameterRange:
    def __init__(self):
        self.estimate = None
        self.left = 0
        self.right = 0


class Node:
    """Create node of binary search tree"""
    def __init__(self, pi=None, key=0):
        self.key = key
        self.pi = pi
        self.left_child = None
        self.right_child = None

        self.cost = None
        self.delay = None
        self.close = False  # default node is open

        self.link = ParameterRange()
        self.noncoverage = ParameterRange()


class Tree:
    """Binary search tree for an optimal placement problem. """
    def __init__(self):
        self.top = None
        self.graph = nx.DiGraph()
        self.unchecked_node = list()  # Stack of unchecked right child nodes
        self.node_keys = list()
        self._key_counter = 0  # Stack of all nodes

    def initiate(self,
                 place: Tuple[float],
                 right_gtw_place: float,
                 cov: np.ndarray) -> None:
        """
        Initiate of binary tree

        Parameters
        ----------
        place - placement points
        right_gtw_place - coordinate of right gateway
        cov - coverage of stations
        """
        """ get init estimate and node init node """
        pi = np.ones([len(place), len(cov)]) * np.inf
        key = self._key_counter
        self.node_keys.append(key)
        self.top = Node(pi, key)
        self.top.noncoverage.estimate = max(right_gtw_place - 2*sum(cov), 0)
        self.top.cost = 0
        self.top.delay = 0
        self.graph.add_node(self.top.key)

    def is_possible_to_add_new_nodes(self, node: Node) -> bool:
        """
        Check the possibility of node adding

        Parameters
        ----------
        node - current node

        Returns
        -------
            True, if it is possible to add new nodes;
            False - otherwise
        """

        sum_by_row = node.pi.sum(axis=1)
        forbidden_place = sum_by_row[np.where(sum_by_row == 0)]
        if node.pi.shape[0] == len(forbidden_place):
            return False
        if len(self.unchecked_node) == 0 and node.close is True:
            return False
        return True

    @staticmethod
    def get_indices(pi: np.ndarray) -> List[float]:
        """
        Get station j, that we can place to the placement i.
        Finding empty place and empty station.

        Parameters
        ----------
            - pi matrix of splitting parameter

        Returns
        -------
            index of placement point and index of station.
        """

        # that Station j is placed on Placement Point i
        row, col = np.where(pi == 1)
        place_index = None
        sta_index = None
        loop_break = False
        for i in range(pi.shape[0]):
            if loop_break:
                break
            for j in range(pi.shape[1]):
                if (i not in row) and (j not in col):
                    if pi[i, j] != 0:
                        place_index = i
                        sta_index = j
                        loop_break = True
                        break

        return [place_index, sta_index]

    def add_left_node(self, i: int, j: int, parent: Node) -> None:
        """
        Add new left child node of tree

        Parameters
        ----------
        i - index of placement point
        j - index of station
        parent - node of tree

        Returns
        -------
            new left child node
        """
        left_pi = parent.pi.copy()
        left_pi[i, j] = 1

        self._key_counter += 1
        left_child_key = self._key_counter

        parent.left_child = Node(left_pi, left_child_key)
        self.node_keys.append(left_child_key)

        self.graph.add_edge(parent.key, left_child_key)

    def add_right_node(self, i: int, j: int, parent: Node) -> None:
        """
        Add new right child node of tree

        Parameters
        ----------
        i - index of placement point
        j - index of station
        parent - node of tree

        Returns
        -------
            new right child node
        """
        right_pi = parent.pi.copy()
        right_pi[i, j] = 0

        self._key_counter += 1  # Right Child Key is equal to Left Child Key + 1
        right_child_key = self._key_counter

        parent.right_child = Node(right_pi, right_child_key)
        self.node_keys.append(right_child_key)
        self.graph.add_edge(parent.key, right_child_key)
        self.unchecked_node.append(parent.right_child)
