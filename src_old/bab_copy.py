# """
# 16th of October
# A Problem of Optimal Location of Given Set of Base Stations in Wireless
# Networks with Linear Topology
#
# Branch And Bound Algorithm For Binary Search Tree
# """
# import networkx as nx
# import numpy as np
#
# from collections import deque
# from src_old.table import Table
# from src_old.input import placement, gateway_placement, cost_limit, delay_limit
# from src_old.input import sta, arival_rate
# from src_old.figure import draw
#
#
# class ParameterRange:
#     def __init__(self):
#         self.left = 0
#         self.right = 0
#
#
# class Node:
#     """Create node of binary search tree"""
#     def __init__(self, pi=None, key=0):
#         self.key = key
#         self.pi = pi
#         self.left = None
#         self.right = None
#         self.noncov_estimate = None
#         self.comm_dist = ParameterRange()
#         self.noncov = ParameterRange()
#         self.cost = 0
#         self.delay = 0
#         self.not_close = True
#
#
# class BST:
#     """Binary search tree for our optimal placement problem"""
#     def __init__(self, place, gateway, cost, delay, station, arival):
#         self.place = place
#         self.gtw = gateway
#         self.cost_limit = cost
#         self.delay_limit = delay
#         self.sta = station
#         self.arival_rate = arival_rate
#         self.cov = tuple(self.sta[i]['r'] for i in self.sta)
#         self.comm_dist = tuple(self.sta[i]['R'] for i in self.sta)
#         self.cost = tuple(self.sta[i]['c'] for i in self.sta)
#         self.departure_rate = tuple(self.sta[i]['mu'] for i in self.sta)
#         self.top = None
#         self.graph = nx.DiGraph()
#         self.table = Table()
#         self.unchecked_node = deque()  # Stack of unchecked right child nodes
#         self.nodes = deque()  # Stack of all nodes
#
#     def get_indices(self, pi):
#         """
#         get station j, that we can place to the placement i
#         :param pi: matrix
#         :return: get indices of first empty pi
#         """
#         row, col = np.where(pi == 1)
#         min_a = None
#         min_s = None
#         loop_break = False
#         for i in range(len(self.place)):
#             if loop_break:
#                 break
#             for j in range(len(self.sta)):
#                 if (i not in row) and (j not in col):
#                     if pi[i, j] != 0:
#                         min_a = i
#                         min_s = j
#                         loop_break = True
#                         break
#         return [min_a, min_s]
#
#     @staticmethod
#     def get_child_pi(i, j, node):
#         """get matrix pi for left child node and right child node
#         :param i: placement index
#         :param j: station index
#         :param node: node node
#         :return: left_pi, right_pi
#         """
#         left_pi = node.pi.copy()
#         left_pi[i, j] = 1
#         right_pi = node.pi.copy()
#         right_pi[i, j] = 0
#         return [left_pi, right_pi]
#
#     def is_able2place(self, node):
#         """
#
#         :param node: current node
#         :return: True, if it is able to place; False - otherwise
#         """
#         sum_by_row = node.pi.sum(axis=1)
#         forbidden_place = sum_by_row[np.where(sum_by_row == 0)]
#         if len(self.place) == len(forbidden_place):
#             return False
#         if len(self.unchecked_node) == 0 and node.not_close is False:
#             return False
#         return True
#
#     @staticmethod
#     def _in_range(place1, place2, communication_distance):
#         """check whether 'first' and 'second' position is in range """
#         return abs(place1 - place2) <= communication_distance
#
#     def is_able_exist(self):
#         """ checking the existence of feasible solution """
#         max_range = max(self.comm_dist)
#         max_range_index = self.comm_dist.index(max_range)
#
#         without_max_range = tuple(self.comm_dist[i]
#                                   for i in range(len(self.comm_dist))
#                                   if i != max_range_index)
#         max_range_2 = max(without_max_range)
#
#         last = self.gtw[-1]
#
#         if not (self._in_range(0, self.place[0], max_range) and
#                 self._in_range(last, self.place[-1], max_range)):
#             return False
#
#         for i in range(len(self.place) - 1):
#             if not self._in_range(self.place[i], self.place[i+1], max_range_2):
#                 return False
#
#         return True
#
#     def initiate_tree(self):
#         """ get init estimate and node init node """
#         pi = np.ones([len(self.place), len(self.sta)]) * np.inf
#         key = 0
#         self.nodes.append(key)
#         self.top = Node(pi, key)
#         self.graph.add_node(self.top.key)
#         root = self.top
#         init_noncoverage = sum([2 * i for i in self.cov])
#         self.top.noncov_estimate = max(self.gtw[-1] - init_noncoverage, 0)
#         self.table.add(np.inf, np.inf, np.inf, self.top.noncov_estimate, key)
#         self.table.record.append(self.gtw[-1])
#         return [root, key]
#
#     def is_able_link_left(self, node, p_ind, s_ind):
#         """
#
#         :param node: current node
#         :param p_ind: index of placement
#         :param s_ind: index of station
#         :return: -True if communication distance is more than the distance to
#          the left station, -False otherwise
#         """
#         node.right.comm_dist.left = node.comm_dist.left
#         current_place = self.place[p_ind]
#         current_comm_dist = self.comm_dist[s_ind]
#
#         if 1 in node.pi:
#             i, j = np.where(node.pi == 1)
#             left_place = self.place[i[-1]]
#             left_comm_dist = self.comm_dist[j[-1]]
#             if not self._in_range(left_place, current_place, left_comm_dist):
#                 node.not_close = False
#                 return node.not_close
#         else:
#             left_place = self.gtw[0]
#         if not self._in_range(left_place, current_place, current_comm_dist):
#             node.not_close = False
#             return node.not_close
#         node.left.comm_dist.left = node.comm_dist.left + (current_place -
#                                                           left_place)
#
#         return node.not_close
#
#     def is_able_link_right(self, node, p_ind, s_ind):
#         """
#         check right of placement point
#         :param node: current node
#         :param p_ind: index of placement
#         :param s_ind: index of station
#         :return: (bool) -True if link range is greater than distance or
#             False otherwise
#         """
#         node.right.comm_dist.right = node.comm_dist.right
#
#         current_place = self.place[p_ind]
#         current_comm_dist = self.comm_dist[s_ind]
#
#         _, j = np.where(node.pi == 1)
#         placed_comm_dist = [self.comm_dist[i] for i in j] + [current_comm_dist]
#
#         if current_place == self.place[-1] or \
#            len(placed_comm_dist) == len(self.comm_dist):
#             right_place = self.gtw[-1]
#         else:
#             right_place = self.place[p_ind+1]
#             unplaced_comm_dist = [self.comm_dist[i]
#                                   for i in range(len(self.comm_dist))
#                                   if (i not in j) and i != s_ind]
#             max_comm_dist = max(unplaced_comm_dist)
#             if not self._in_range(right_place, current_place, max_comm_dist):
#                 node.not_close = False
#                 return node.not_close
#
#         if not self._in_range(right_place, current_place, current_comm_dist):
#             node.not_close = False
#             return node.not_close
#         node.left.comm_dist.right = current_comm_dist
#         return node.not_close
#
#     def is_able_within_unplaced(self, node, p_ind, s_ind):
#         """
#         check unplaced station and right places
#         :param node: current node
#         :param p_ind: index of placement
#         :param s_ind: index of station
#         :return: -True if link range of unplaced station is greater than
#             distance or False otherwise
#         """
#         if node.key == 8:
#             a = 1
#         _, j = np.where(node.pi == 1)
#         unplaced = [self.comm_dist[i]
#                     for i in range(len(self.comm_dist))
#                     if (i not in j) and i != s_ind]
#
#         if len(unplaced) == 1:
#             node.not_close = False
#             if p_ind is self.place.index(self.place[-1]):
#                 node.not_close = self._in_range(self.place[p_ind], self.gtw[-1],
#                                                 unplaced[0])
#             else:
#                 for right_p in (self.place[p_ind+1:]):
#                     node.not_close = self._in_range(self.place[p_ind],
#                                                     right_p,
#                                                     unplaced[0]) and\
#                                       self._in_range(right_p,
#                                                      self.gtw[-1],
#                                                      unplaced[0])
#                     if node.not_close:
#                         return node.not_close
#                 return node.not_close
#
#         if len(unplaced) > 1:
#             max_range = max(unplaced)
#             unplaced.remove(max_range)
#             max_range_2 = max(unplaced)
#
#             for i in range(len(self.place[p_ind+1:])):
#                 if i == len(self.place) - 1:
#                     if not self._in_range(self.gtw[-1],
#                                           self.place[i],
#                                           max_range):
#                         node.not_close = False
#                         return node.not_close
#                 else:
#                     if not self._in_range(self.place[i+1],
#                                           self.place[i],
#                                           max_range_2):
#                         node.not_close = False
#                         return node.not_close
#         return node.not_close
#
#     def get_placement(self, node):
#         """
#
#         :param node: tree node
#         :return: to print placed stations
#         """
#         i, j = np.where(node.pi == 1)
#         placed_sta = [np.inf] * len(self.place)
#         for k in range(len(i)):
#             placed_sta[i[k]] = j[k] + 1
#         draw(self.graph)
#         print('Placed stations = ', placed_sta,
#               ', Noncoverage = ', self.table.record[-1],
#               ', Cost =  ', node.cost,
#               ', Delay =  ', node.delay,
#               ', Node number =  ', node.key)
#
#     def check_cost(self, node):
#         if node.cost > self.cost_limit:
#             return False
#         return True
#
#     def check_delay(self, node):
#         if node.delay > self.delay_limit:
#             return False
#         return True
#
#     def check_estimate(self, node):
#         """
#         check able to close a node and add new record
#         :param node:
#         :return: True or False
#         """
#         if node.noncov_estimate < self.table.record[-1]:
#             if (node.comm_dist.left + node.comm_dist.right) >= \
#                     (self.gtw[1]-self.gtw[0]):
#                 node_noncov = node.noncov.left + node.noncov.right
#                 if ((node_noncov < self.table.record[-1]) and
#                         self.check_cost(node) and self.check_delay(node)):
#                     self.table.record.append(node_noncov)
#                     self.get_placement(node)
#             return True
#         else:
#             return False
#
#     def check_link(self, node, i, j):
#         """
#         Check link conditions
#         :param node: current node
#         :param i: index of placement
#         :param j: index of station
#         :return: True or False
#         """
#         if self.is_able_link_left(node, i, j) and \
#                 self.is_able_link_right(node, i, j) and \
#                 self.is_able_within_unplaced(node, i, j):
#             return True
#
#         return False
#
#     @staticmethod
#     def noncov_inrange(place1, place2, cov1, cov2):
#         """
#         Calculate estimate of noncoverage in range between place1 and place2
#         :param place1:
#         :param place2:
#         :param cov1:
#         :param cov2:
#         :return: Noncoverage between two placed station
#         """
#         dist = abs(place2 - place1)
#         cov = cov1 + cov2
#         return max([dist - cov, 0])
#
#     def noncoverage(self, p_ind, s_ind, node):
#         """
#         calculate the estimates of noncoverage
#         :param p_ind: index of placement
#         :param s_ind: index of station
#         :param node: parent node
#         :return: Noncoverage estimate
#         """
#         i, j = np.where(node.pi == 1)
#         if len(i) == 0:
#             place1 = self.gtw[0]
#             cov1 = 0
#         else:
#             place1 = self.place[i[-1]]
#             cov1 = self.cov[j[-1]]
#         # left noncoverage
#         left_noncov = node.noncov.left + \
#                       self.noncov_inrange(place1,
#                                           self.place[p_ind],
#                                           cov1,
#                                           self.cov[s_ind])
#         # right noncoverage
#         unplaced_cov = [self.cov[i] for i in range(len(self.cov))
#                         if (i not in j) and (i != s_ind)]
#
#         unbusy_place = [self.place[j] for j in range(len(self.place))
#                         if (j not in i) and (j != p_ind)]
#         if len(unplaced_cov) > len(unbusy_place):
#             cov = list(self.cov)
#             cov.sort()
#             max_cov = cov[-1:-(len(unbusy_place)+1):-1]
#             unplaced_cov = [self.cov[i] for i in range(len(max_cov))
#                             if (i not in j) and (i != s_ind)]
#
#         right_noncov = self.noncov_inrange(self.place[p_ind],
#                                            self.gtw[-1],
#                                            self.cov[s_ind],
#                                            sum(2*unplaced_cov))
#         # node noncoverage
#         node.left.noncov.left = node.noncov.left + left_noncov
#         node.left.noncov.right = (self.gtw[-1] -
#                                   self.place[p_ind]) - self.cov[s_ind]
#
#         return left_noncov + right_noncov
#
#     def add_delay(self, j):
#         rho = self.arival_rate / self.departure_rate[j]
#         mean_system_size = rho / (1 - rho)
#         return mean_system_size / self.arival_rate
#
#     def add_child_nodes(self, node, key):
#         """
#         To add new child nodes
#         :param node: node node
#         :param key: node number
#         :return:
#         """
#         i, j = self.get_indices(node.pi)
#         if [i, j] != [None, None]:
#             left_pi, right_pi = self.get_child_pi(i, j, node)
#
#             # add left node
#             key += 1
#             self.nodes.append(key)
#             node.left = Node(left_pi, key)
#             node.left.noncov_estimate = self.noncoverage(i, j, node)
#             node.left.cost = node.cost + self.cost[j]
#             node.left.delay = node.delay + self.add_delay(j)
#             self.graph.add_edge(node.key, node.left.key)
#             self.table.add(i, j, node.left.pi[i, j],
#                            node.left.noncov_estimate, key)
#             draw(self.graph)
#
#             # add right node
#             key += 1
#             self.nodes.append(key)
#             node.right = Node(right_pi, key)
#             node.right.noncov_estimate = node.noncov_estimate
#             node.right.noncov.left = node.noncov.left
#             node.right.noncov.right = node.noncov.right
#             node.right.cost = node.cost
#             node.right.delay = node.delay
#             self.graph.add_edge(node.key, node.right.key)
#             self.table.add(i, j, node.left.pi[i, j],
#                            node.right.noncov_estimate, key)
#
#             draw(self.graph)
#             self.unchecked_node.append(node.right)
#
#             if (self.check_link(node, i, j) and
#                     self.check_estimate(node.left)):
#                 return [node.left, key]
#             self.unchecked_node.pop()
#             return [node.right, key]
#         else:
#             if len(self.unchecked_node) != 0:
#                 node = self.unchecked_node[-1]
#                 self.unchecked_node.pop()
#
#         return [node, self.nodes[-1]]
#
#     def search(self):
#         """
#         Search binary tree solution
#         :return: record of non-coverage
#         """
#         assert self.is_able_exist(), 'There is not solution'
#         [parent, key] = self.initiate_tree()
#         while self.is_able2place(parent):
#             parent, key = self.add_child_nodes(parent, key)
#
#
# solution = BST(placement, gateway_placement, cost_limit, delay_limit, sta,
#                arival_rate)
# solution.search()
# # draw(solution.graph)
# print('record =  ', solution.table.record[-1])
