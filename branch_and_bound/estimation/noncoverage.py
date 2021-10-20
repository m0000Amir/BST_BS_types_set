from binary_search.tree import Node
from branch_and_bound.estimation.problem.ilp import ILP
from branch_and_bound.estimation.problem.knapsack import KnapsackProblem
from branch_and_bound.estimation.problem.solver import solve_ilp_problem
from branch_and_bound.estimation.problem.solver import solve_lp_problem
from network.performance_characteristics import noncoverage_between_station

from typing import Tuple, Any

import numpy as np
from matlab.engine import MatlabEngine


def get_noncoverage_estimate(p: int, s: int, node: Node,
                             gtw: Tuple[float], place: Tuple[Any],
                             cov: np.ndarray, cost: Tuple[Any],
                             cost_limit: float,
                             engine: MatlabEngine,
                             flag: str = 'ILP') -> Tuple[float, bool]:
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
    :param flag: MatLab engine

    :return: Noncoverage estimate
    """
    i, j = np.where(node.pi == 1)

    vacant_stations_coverage = [cov[i] for i in range(len(cov))
                                if (i not in j) and (i != s)]
    vacant_stations_cost = [cost[i] for i in range(len(cov))
                            if (i not in j) and (i != s)]

    vacant_placement_points = [place[j] for j in range(len(place))
                               if (j not in i) and (j != p)]
    node.left_child.noncoverage.right = max((gtw[-1] - place[p]) - cov[s], 0)
    if (len(vacant_stations_coverage) is 0) or (len(vacant_placement_points) is 0):
        right_noncoverage_estimate = node.left_child.noncoverage.right
    else:
        remaining_cost = cost_limit - node.cost - cost[s]

        if flag == 'knapsack':
            problem = KnapsackProblem(vacant_stations_coverage,
                                      vacant_stations_cost,
                                      remaining_cost)
        # elif flag == 'ILP' or flag == 'LP':
        else:
            problem = ILP(vacant_stations_coverage,
                          vacant_stations_cost,
                          remaining_cost,
                          vacant_placement_points)

        if flag == 'knapsack' or flag == 'ILP':
            right_cov_estimate = solve_ilp_problem(problem, engine)
        # elif flag == 'LP':
        else:
            right_cov_estimate = solve_lp_problem(problem)

        right_noncoverage_estimate = noncoverage_between_station(
            place[p], gtw[1], cov[s], right_cov_estimate)
    novcov_estimate = (node.left_child.noncoverage.left +
                       right_noncoverage_estimate)
    return novcov_estimate
