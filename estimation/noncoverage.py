from binary_search.tree import Node
from estimation.problem.int_lin_prog import ILP
from estimation.problem.knapsack import KnapsackProblem
from estimation.problem.solver import solve_milp_problem, solve_linprog_problem

from typing import Tuple, Any

import numpy as np


def noncov_btwn_sta(place1: float, place2: float,
                    cov1: float, cov2: float) -> float:
    """
    Calculate noncoverage between place1 and place2
    :param place1:
    :param place2:
    :param cov1:
    :param cov2:
    :return: Noncoverage between two placed station
    """
    dist = abs(place2 - place1)
    cov = cov1 + cov2
    return max([dist - cov, 0])


def get_noncoverage(p: int, s: int, node: Node,
                    gtw: Tuple[float], place: Tuple[Any],
                    cov: np.ndarray, cost: Tuple[Any],
                    cost_limit: float, engine) -> Tuple[float, bool]:
    """
    Calculate estimates of noncoverage

    :param p: index of placement
    :param s: index of station
    :param node: parent node
    :param gtw: gateways coordinates
    :param place: placement coordinates
    :param cov: stations coverage radius
    :param cost: stations cost
    :param cost_limit: given cost limit of problem
    :param engine: MatLab engine

    :return: Noncoverage estimate
    """
    i, j = np.where(node.pi == 1)

    if len(i) == 0:  # searching is just started
        left_sta_place = gtw[0]
        left_sta_cov = 0
    else:
        left_sta_place = place[i[-1]]
        left_sta_cov = cov[j[-1]]

    # left noncoverage
    left_noncov = node.noncov.left + noncov_btwn_sta(left_sta_place,
                                                     place[p],
                                                     left_sta_cov,
                                                     cov[s])
    node.left_child.noncov.left = left_noncov
    # right noncoverage
    unbusy_sta_cov = [cov[i] for i in range(len(cov))
                      if (i not in j) and (i != s)]
    unbusy_sta_cost = [cost[i] for i in range(len(cov))
                       if (i not in j) and (i != s)]

    unbusy_place = [place[j] for j in range(len(place))
                    if (j not in i) and (j != p)]
    node.left_child.noncov.right = max((gtw[-1] - place[p]) - cov[s], 0)
    if (len(unbusy_sta_cov) is 0) or (len(unbusy_place) is 0):
        right_noncov_estimate = node.left_child.noncov.right
    else:
        remaining_cost = cost_limit - node.cost - cost[s]
        # TODO: change flag condition
        flag = 'ILP'
        if flag =='knapsack':
            problem = KnapsackProblem(unbusy_sta_cov, unbusy_sta_cost,
                                      remaining_cost)
            problem.prepare()
        elif flag == 'ILP' or flag == 'LP':
            problem = ILP(unbusy_sta_cov, unbusy_sta_cost, remaining_cost,
                          unbusy_place)
            problem.prepare()
        if flag == 'knapsack' or flag == 'ILP':
            right_cov_estimate = solve_milp_problem(problem, engine)
        elif flag == 'LP':
            right_cov_estimate = solve_linprog_problem(problem)

        right_noncov_estimate = noncov_btwn_sta(place[p], gtw[1], cov[s],
                                                right_cov_estimate)
    novcov_estimate = left_noncov + right_noncov_estimate
    return novcov_estimate
